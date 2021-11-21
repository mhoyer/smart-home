import common
import time
import appdaemon.plugins.hass.hassapi as hass

class BathRoomAutomation(hass.Hass):

  ceil_lights = [
    "light.bath_light_01",
    "light.bath_light_02",
    "light.bath_light_03",
    "light.bath_light_04"
  ]

  ambient_light = "light.bath_mirror_light"

  def initialize(self):
    self.listen_state(self.on_light_switch_press, "sensor.bath_switch_action", attribute="action")
    self.listen_state(self.on_bath_motion, "binary_sensor.bath_motion_occupancy", attribute="state")


  def on_bath_motion(self, entity, attribute, old, new, kwargs):
    self.log(f"Some motion in bath room: {attribute}={new}.")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    common.update_last_action()

    if new == "off":
      if self.get_state(self.ceil_lights[0]) == "on":
        self.turn_lights_off()
      else:
        self.turn_lights_on()
    elif new == "on":
      if self.get_state(self.ambient_light) == "on":
        self.turn_off(self.ambient_light)
      else:
        self.turn_on(self.ambient_light)

  def turn_lights_on(self):
    for light in self.ceil_lights:
      self.turn_on(light)
      time.sleep(0.2)

  def turn_lights_off(self):
    for light in self.ceil_lights:
      self.turn_off(light)
      time.sleep(0.2)
