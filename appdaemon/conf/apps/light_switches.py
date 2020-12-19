import appdaemon.plugins.hass.hassapi as hass

class LightSwitches(hass.Hass):

  def initialize(self):
    self.wire_up_toggle(
      switches=["sensor.sleep_switch_action"],
      action="on",
      lights=["light.sleep_light_light"]
    )
    self.wire_up_toggle(
      switches=["sensor.kitchen_switch_action"],
      action="on",
      lights=["light.kitchen_light_light"]
    )
    self.wire_up_toggle(
      switches=["sensor.kitchen_switch_action"],
      action="off",
      lights=["light.kitchen_light_corner_light"]
    )

  def wire_up_toggle(self, switches, action, lights):
    def toggle(entity, attribute, old, new, kwargs):
      if new != action: return

      self.log(f'"{entity}" fired [action="{new}"]')
      turn_fn = self.turn_on

      if self.get_state(lights[0]) == "on":
        turn_fn = self.turn_off

      for light in lights:
        self.log(f'  {turn_fn.__name__}: {light}')

        turn_fn(light)

    for entity in switches:
      self.log(f'Register "{entity}" to toggle when [action="{action}"]:')
      for light in lights:
        self.log(f'  + "{light}"')
      self.listen_state(toggle, entity, attribute="action")
