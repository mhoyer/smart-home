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
  ambient_light_night_attr = {"brightness": 1, "rgb_color": [255,129,0]}
  last_ambient_light_attr = None

  def initialize(self):
    self.listen_state(self.on_light_switch_press, "sensor.bath_switch_action", attribute="action")
    self.listen_state(self.on_bath_motion, "binary_sensor.bath_motion_occupancy", attribute="state")
    # self.log(f"==> {self.get_state(self.ambient_light, 'attributes')}")


  def on_bath_motion(self, entity, attribute, old, new, kwargs):
    if self.sun_up():
      return

    self.log(f"Some motion in bath room: {attribute}={new}.")

    amb_state = self.get_state(self.ambient_light, 'state')
    if new == 'on':
      if amb_state == 'on':
        return


    elif new == 'off':
      if amb_state == 'off':
        return



  def save_current_ambstate(self):
    amb_attr = self.get_state(self.ambient_light, 'attributes')

    if amb_attr['brightness'] == self.ambient_light_night_attr['brightness'] \
    and amb_attr['rgb_color'] == self.ambient_light_night_attr['rgb_color']:
      self.log('We are already in night mode!')
    else:
      self.log('Turning on night light')
    #  self.last_ambient_light_attr = {"brightness": amb_attr["brightness"], "rgb_color": amb_attr["rgb_color"]}

    # self.log(f"==> {self.get_state(self.ambient_light, 'all')}")
    # self.turn_on(self.ambient_light, color_mode="color_temp", brightness=1, color_temp=524)
    # self.turn_on(self.ambient_light, brightness=40, rgb_color=[255,130,0])
    # self.turn_on(self.ambient_light, brightness=1, color_temp=526)
    # self.set_state(self.ambient_light, state="on", attributes={"brightness": 50, "color_temp": 524})

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
