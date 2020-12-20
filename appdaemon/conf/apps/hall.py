import appdaemon.plugins.hass.hassapi as hass
import time

class HallAutomation(hass.Hass):

  lights = [
    "light.hall_light_01",
    "light.hall_light_02",
    "light.hall_light_03"
  ]

  def initialize(self):
    self.listen_state(self.on_light_switch_press, "sensor.hall_switch_01_action", attribute="action")
    self.listen_state(self.on_light_switch_press, "sensor.hall_switch_02_action", attribute="action")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    if new != "on": return

    if self.get_state(self.lights[0]) == "on":
      self.turn_lights_off()
    else:
      self.turn_lights_on()

  def on_main_door_contact(self, entity, attribute, old, new, kwargs):
    action = self.turn_off if new else self.turn_on
    list(map(action, self.lights))

  def turn_lights_on(self):
    for light in self.lights:
      self.turn_on(light)
      time.sleep(0.2)

  def turn_lights_off(self):
    for light in self.lights:
      self.turn_off(light)
      time.sleep(0.2)
