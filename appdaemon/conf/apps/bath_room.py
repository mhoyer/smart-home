import appdaemon.plugins.hass.hassapi as hass

class BathRoomAutomation(hass.Hass):

  ceil_lights = [
    "light.bath_light_01",
    "light.bath_light_02",
    "light.bath_light_03",
    "light.bath_light_04"
  ]

  ambient_lights = ["light.bath_mirror_light"]

  def initialize(self):
    self.listen_state(self.on_light_switch_press, "sensor.bath_switch_action", attribute="action")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    if new == "off":
      action = self.turn_on
      if self.get_state(self.ceil_lights[0]) == "on":
        action = self.turn_off

      list(map(action, self.ceil_lights))

    elif new == "on":
      action = self.turn_on
      if self.get_state(self.ambient_lights[0]) == "on":
        action = self.turn_off

      list(map(action, self.ambient_lights))
