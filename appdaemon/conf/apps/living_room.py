import appdaemon.plugins.hass.hassapi as hass
import appdaemon.plugins.mqtt.mqttapi as mqtt
import time

class LivingRoomAutomation(hass.Hass, mqtt.Mqtt):

  ceiling_light = "light.living_light_ceiling"
  basket_light = "light.living_basket_light"
  power_switch_fairy_lights = "switch.living_power_switch_fairy_lights"

  ambient_lights = [
    basket_light,
    power_switch_fairy_lights,
  ]

  def initialize(self):
    self.listen_state(self.on_light_switch_press, "sensor.living_switch_action", attribute="action")
    self.listen_state(self.on_movie_mode_change, "input_boolean.appdaemon_movie_mode", attribute="state")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    if new != "on": return

    if self.get_state(self.ambient_lights[0]) == "on":
      list(map(self.turn_off, self.ambient_lights))
      self.turn_off(self.ceiling_light)
    else:
      list(map(self.turn_on, self.ambient_lights))

  def on_movie_mode_change(self, entity, attribute, old, new, kwargs):
    if new == "on":
      self.mqtt_publish("hushboxctrl/movie_mode", "on")
      self.turn_off(self.ceiling_light)
      time.sleep(0.5)
      self.turn_off(self.basket_light)
    else:
      self.mqtt_publish("hushboxctrl/movie_mode", "off")
      self.turn_on(self.basket_light)
      time.sleep(0.5)
      self.turn_on(self.power_switch_fairy_lights)
