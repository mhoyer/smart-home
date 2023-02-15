import common
import appdaemon.plugins.hass.hassapi as hass
import appdaemon.plugins.mqtt.mqttapi as mqtt

light_switch = "sensor.kitchen_switch_action"
ceiling_light = "light.kitchen_light"
corner_light = "light.kitchen_light_corner"
fairy_lights = "switch.power_switch_01"
hifi_power_button = "input_button.kitchen_power_hifi"

class KitchenAutomation(hass.Hass, mqtt.Mqtt):
  def initialize(self):
    self.listen_state(self.on_light_switch_press, light_switch, attribute="action")
    self.listen_state(self.on_hifi_power_toggle, hifi_power_button, attribute="state")
    # it's actually the pixel 2 charger attached here:
    self.run_daily(self.daily_turn_on_lights, "23:30:00")
    self.run_daily(self.daily_turn_off_lights, "00:30:00")

  def on_hifi_power_toggle(self, entity, attribute, old, new, kwargs):
    self.mqtt_publish("squeezy_kitchen/hifi_power_toggle", "on")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    common.update_last_action()

    if new == "on":
      if self.get_state(ceiling_light) == "off":
        self.turn_on(ceiling_light)
      else:
        self.turn_off(ceiling_light)
    elif new == "off":
      if self.get_state(corner_light) == "off":
        self.turn_on(corner_light)
      else:
        self.turn_off(corner_light)

  def daily_turn_on_lights(self, *args, **kwargs):
    self.turn_on(fairy_lights)

  def daily_turn_off_lights(self, *args, **kwargs):
    self.turn_off(fairy_lights)
