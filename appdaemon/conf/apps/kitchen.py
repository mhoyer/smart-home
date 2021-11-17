import common
import appdaemon.plugins.hass.hassapi as hass

class KitchenAutomation(hass.Hass):

  main_light = "light.kitchen_light"
  corner_light = "light.kitchen_light_corner"
  fairy_lights = "switch.power_switch_01"

  def initialize(self):
    self.listen_state(self.on_light_switch_press, "sensor.kitchen_switch_action", attribute="action")
    self.run_daily(self.daily_turn_off_lights, "00:30:00")


  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    common.update_last_action()

    if new == "on":
      if self.get_state(self.main_light) == "off":
        self.turn_on(self.main_light)
      else:
        self.turn_off(self.main_light)
    elif new == "off":
      if self.get_state(self.corner_light) == "off":
        self.turn_on(self.corner_light)
      else:
        self.turn_off(self.corner_light)

  def daily_turn_off_lights(self, *args, **kwargs):
    self.turn_off(self.fairy_lights)
