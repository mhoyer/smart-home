import common
import time
import appdaemon.plugins.hass.hassapi as hass

light_group_entity = "input_boolean.appdaemon_light_group_bath"
ceiling_lights = [
  "light.bath_light_01",
  "light.bath_light_02",
  "light.bath_light_03",
  "light.bath_light_04"
]
mirror_light = "light.bath_mirror_light"

class BathRoomAutomation(hass.Hass):
  def initialize(self):
    self.listen_state(self.on_light_switch_press, "sensor.bath_switch_action", attribute="action")
    self.listen_state(self.on_bath_motion, "binary_sensor.bath_motion_occupancy", attribute="state")
    self.listen_state(self.on_light_group_toggle, light_group_entity, attribute="state")

  def on_bath_motion(self, entity, attribute, old, new, kwargs):
    self.log(f"Some motion in bath room: {attribute}={new}.")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    common.update_last_action()

    if new == "off":
      self.toggle(light_group_entity)
    elif new == "on":
      if self.get_state(mirror_light) == "on":
        self.turn_off(mirror_light)
      else:
        self.turn_on(mirror_light)

  def on_light_group_toggle(self, entity, attribute, old, new, kwargs):
    common.update_last_action()

    if self.get_state(ceiling_lights[0]) == new:
      return

    if new == "on":
      for light in ceiling_lights:
        self.turn_on(light)
        time.sleep(0.2)
    else:
      for light in ceiling_lights:
        self.turn_off(light)
        time.sleep(0.2)
