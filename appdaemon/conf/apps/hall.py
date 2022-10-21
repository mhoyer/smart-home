from datetime import datetime, timedelta
import time
import common
import appdaemon.plugins.hass.hassapi as hass

light_group_entity = "input_boolean.appdaemon_light_group_hall"
door_sensor = "binary_sensor.hall_door_sensor_contact"
switch_entities = [
  "sensor.hall_switch_01_action",
  "sensor.hall_switch_02_action"
]
ceiling_lights = [
  "light.hall_light_01",
  "light.hall_light_02",
  "light.hall_light_03"
]

class HallAutomation(hass.Hass):
  def initialize(self):
    self.auto_lights_off_handle = None
    self.last_switch_action = datetime.now()

    self.listen_state(self.on_light_switch_press, switch_entities, attribute="action")
    self.listen_state(self.on_light_group_toggle, light_group_entity, attribute="state")
    self.listen_state(self.on_main_door_contact, door_sensor, attribute="state")

    ### to fix/workaround https://github.com/AppDaemon/appdaemon/issues/1576
    self.run_every(self.issue_1567, "now", 60)

  def issue_1567(self, kwargs):
  #   #self.log(f"heartbeat: {self.AD.sched.now}")
    return

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    if (datetime.now()-self.last_switch_action).total_seconds() > 1:
      self.toggle(light_group_entity)
    self.last_switch_action = datetime.now()

  def on_light_group_toggle(self, entity, attribute, old, new, kwargs):
    common.update_last_action()
    self.cancel_auto_lights_off_timer()

    self.log(f"{self.get_state(ceiling_lights[0])} == {new}")

    if self.get_state(ceiling_lights[0]) == new:
      return

    if new == "on":
      self.turn_lights_on()
    else:
      self.turn_lights_off()

  def on_main_door_contact(self, entity, attribute, old, new, kwargs):
    self.log(f"Someone opened the door. sun_up={self.sun_up()}, sunset={self.sunset()}, sunrise={self.sunrise()}, now={self.get_now()}.")

    if self.sun_up():
      return

    if new == "on":
      since_last_action = datetime.now() - common.last_action
      self.log(f"Last action happend {int(since_last_action.total_seconds())}s ago.")

      if since_last_action > timedelta(seconds = 300) \
      and self.get_state(ceiling_lights[0]) == "off":
        self.turn_on(light_group_entity)

        self.cancel_auto_lights_off_timer()
        self.auto_lights_off_handle = self.run_in(self.turn_lights_off, 300)

    common.update_last_action()

  def cancel_auto_lights_off_timer(self):
    if self.auto_lights_off_handle:
      self.cancel_timer(self.auto_lights_off_handle)
      self.auto_lights_off_handle = None

  def auto_turn_lights_off(self, kwargs=None):
    self.turn_off(light_group_entity)

  def turn_lights_on(self, kwargs=None):
    for light in ceiling_lights:
      self.turn_on(light)
      time.sleep(0.2)

  def turn_lights_off(self, kwargs=None):
    for light in ceiling_lights:
      self.turn_off(light)
      time.sleep(0.2)
