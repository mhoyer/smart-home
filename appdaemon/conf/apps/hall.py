import appdaemon.plugins.hass.hassapi as hass

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

    action = self.turn_off if self.get_state(self.lights[0]) == "on" else self.turn_on
    list(map(action, self.lights))

  def on_main_door_contact(self, entity, attribute, old, new, kwargs):
    action = self.turn_off if new else self.turn_on
    list(map(action, self.lights))
