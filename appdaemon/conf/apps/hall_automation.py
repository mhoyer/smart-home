import appdaemon.plugins.hass.hassapi as hass

class HallAutomation(hass.Hass):

  def initialize(self):
    self.listen_state(self.on_main_door_contact, "binary_sensor.hall_door_sensor_contact", attribute="contact")

  def on_main_door_contact(self, entity, attribute, old, new, kwargs):
    # if new != "true": return

    self.log(f'"{entity}" fired [action="{new}"]')
    # turn_fn = self.turn_on

    # if self.get_state(lights[0]) == "on":
    # turn_fn = self.turn_off

    # for light in lights:
    # self.log(f'  {turn_fn.__name__}: {light}')

    # turn_fn(light)
