from datetime import datetime, timedelta
import time
import common
import appdaemon.plugins.hass.hassapi as hass

class HallAutomation(hass.Hass):

  lights = [
    "light.hall_light_01",
    "light.hall_light_02",
    "light.hall_light_03"
  ]

  def initialize(self):
    self.auto_lights_off_handle = None

    self.listen_state(self.on_light_switch_press, "sensor.hall_switch_01_action", attribute="action")
    self.listen_state(self.on_light_switch_press, "sensor.hall_switch_02_action", attribute="action")

    self.listen_state(self.on_main_door_contact, "binary_sensor.hall_door_sensor_contact", attribute="state")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    if new != "on":
      return

    common.update_last_action()
    self.cancel_auto_lights_off_timer()

    if self.get_state(self.lights[0]) == "on":
      self.turn_lights_off()
    else:
      self.turn_lights_on()

  def on_main_door_contact(self, entity, attribute, old, new, kwargs):
    if self.sun_up():
      return

    if new == "on":
      since_last_action=datetime.now() - common.last_action
      self.log(f"Someone opened the door. Last action happend {int(since_last_action.total_seconds())}s ago.")
      if since_last_action > timedelta(seconds = 300) \
      and self.get_state(self.lights[0]) == "off":
        self.turn_lights_on()
        self.cancel_auto_lights_off_timer()
        self.auto_lights_off_handle = self.run_in(self.turn_lights_off, 300)

    common.update_last_action()

  def cancel_auto_lights_off_timer(self):
    if self.auto_lights_off_handle:
      self.cancel_timer(self.auto_lights_off_handle)
      self.auto_lights_off_handle = None

  def auto_turn_lights_off(self, kwargs=None):
    self.turn_lights_off()

  def turn_lights_on(self, kwargs=None):
    for light in self.lights:
      self.turn_on(light)
      time.sleep(0.2)

  def turn_lights_off(self, kwargs=None):
    for light in self.lights:
      self.turn_off(light)
      time.sleep(0.2)
