import appdaemon.plugins.hass.hassapi as hass

class LivingRoomAutomation(hass.Hass):

  lights = [
    "light.living_basket_light",
    "switch.living_power_switch_fairy_lights"
  ]

  def initialize(self):
    self.listen_state(self.on_light_switch_press, "sensor.living_switch_action", attribute="action")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    if new != "on": return

    action = self.turn_off if self.get_state(self.lights[0]) == "on" else self.turn_on
    list(map(action, self.lights))
