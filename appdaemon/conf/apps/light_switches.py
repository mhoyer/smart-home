import appdaemon.plugins.hass.hassapi as hass

class LightSwitches(hass.Hass):

  def initialize(self):
    self.listen_state(self.toggle_bath, entity="sensor.bath_switch_action", attribute="action")
    self.listen_state(self.toggle_living, entity="sensor.living_switch_action", attribute="action")

  def toggle_bath(self, entity, attribute, old, new, kwargs):
    self.log(f'{entity}: {new}')
    if new == "off":
      if self.get_state("light.bath_light_01_light") == "off":
        self.turn_on("light.bath_light_01_light")
        self.turn_on("light.bath_light_02_light")
        self.turn_on("light.bath_light_03_light")
        self.turn_on("light.bath_light_04_light")
      else:
        self.turn_off("light.bath_light_01_light")
        self.turn_off("light.bath_light_02_light")
        self.turn_off("light.bath_light_03_light")
        self.turn_off("light.bath_light_04_light")
    if new == "on":
      self.toggle("light.bath_mirror_light_light")

  def toggle_living(self, entity, attribute, old, new, kwargs):
    self.log(f'{entity}: {new}')
    if new == "on":
      self.toggle("light.living_light_ceiling_light")
