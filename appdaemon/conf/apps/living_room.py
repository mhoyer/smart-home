import common
import time
import appdaemon.plugins.hass.hassapi as hass
import appdaemon.plugins.mqtt.mqttapi as mqtt

light_switch_entity = "sensor.living_switch_action"
light_group_entity = "input_boolean.appdaemon_light_group_living"
ceiling_light = "light.living_light_ceiling"
basket_light = "light.living_basket_light"
party_uplight = "light.living_party_uplight"
fairy_lights = "switch.living_power_switch_fairy_lights"
ambient_lights = [
  basket_light,
  party_uplight
]
movie_mode_entity = "input_boolean.appdaemon_movie_mode"
hb_fan_mode = "input_boolean.appdaemon_fan_mode"
hb_fan_speed = "input_number.appdaemon_fan_speed"

class LivingRoomAutomation(hass.Hass, mqtt.Mqtt):
  def initialize(self):
    self.listen_state(self.on_light_switch_press, light_switch_entity, attribute="action")
    self.listen_state(self.on_light_group_toggle, light_group_entity, attribute="state")
    self.listen_state(self.on_movie_mode_change, movie_mode_entity, attribute="state")
    self.listen_state(self.on_fan_mode_change, hb_fan_mode, attribute="state")
    self.listen_state(self.on_fan_speed_change, hb_fan_speed, attribute="state")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    self.toggle(light_group_entity)

  def on_light_group_toggle(self, entity, attribute, old, new, kwargs):
    common.update_last_action()

    if self.get_state(ambient_lights[0]) == new:
      return

    if new == "on":
      self.turn_lights_on()
    else:
      self.turn_lights_off()

  def turn_lights_on(self):
    if self.sun_up(): # to save energy when sun is up and someone presses the switch
      self.turn_on(basket_light)
      return

    for light in ambient_lights:
      self.turn_on(light)

  def turn_lights_off(self):
    self.turn_off(ceiling_light)
    for light in ambient_lights:
      self.turn_off(light)

  recent_basket_light_brightness = 200
  def on_movie_mode_change(self, entity, attribute, old, new, kwargs):
    self.log(f"Change movie mode: {new}")
    if new == "on":
      self.recent_basket_light_brightness = self.get_state(basket_light, attribute="brightness")
      self.turn_on(basket_light, brightness=10)
      self.mqtt_publish("hushboxctrl/movie_mode", "on")
      self.set_state(hb_fan_mode, state="on")
      self.set_state(hb_fan_speed, state=24)
      self.turn_off(party_uplight)
      time.sleep(0.5)
      self.turn_off(ceiling_light)
    else:
      self.mqtt_publish("hushboxctrl/movie_mode", "off")
      self.set_state(hb_fan_mode, state="on")
      self.set_state(hb_fan_speed, state=28)
      self.run_in(self.slow_down_fan, 60)
      self.run_in(self.turn_off_fan, 150)

      self.turn_on(basket_light, brightness=recent_basket_light_brightness)
      time.sleep(2)
      self.turn_on(party_uplight)

  def slow_down_fan(self, *args, **kwargs):
    self.set_state(hb_fan_speed, state=24)

  def turn_off_fan(self, *args, **kwargs):
    self.set_state(hb_fan_speed, state=23)
    self.set_state(hb_fan_mode, state="off")

  def on_fan_mode_change(self, entity, attribute, old, new, kwargs):
    self.log(f"Change fan mode: {new}")
    if new == "on":
      self.mqtt_publish("hushboxctrl/fan_mode", "on")
    else:
      self.mqtt_publish("hushboxctrl/fan_mode", "off")

  def on_fan_speed_change(self, entity, attribute, old, new, kwargs):
    self.log(f"Set fan speed: {new}")
    self.mqtt_publish("hushboxctrl/fan_speed", new)
