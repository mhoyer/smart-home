import appdaemon.plugins.hass.hassapi as hass

class SleepAutomation(hass.Hass):

  def initialize(self):
    self.listen_state(self.open_close_blinds, "sensor.sleep_blinds_ctrl_01_action", attribute="action")
    self.listen_state(self.open_close_blinds, "sensor.sleep_blinds_ctrl_02_action", attribute="action")
    self.run_at_sunrise(self.open_blinds, offset=0)

  def open_close_blinds(self, entity, attribute, old, new, kwargs):
    self.log(f'"{entity}" fired [action="{new}"]')
    if new == "close":
      self.call_service("cover/close_cover", entity_id="cover.sleep_blinds_left_cover")
      self.call_service("cover/close_cover", entity_id="cover.sleep_blinds_right_cover")
    if new == "open":
      self.call_service("cover/open_cover", entity_id="cover.sleep_blinds_left_cover")
      self.call_service("cover/open_cover", entity_id="cover.sleep_blinds_right_cover")

  def open_blinds(self, kwargs):
    self.call_service("cover/open_cover", entity_id="cover.sleep_blinds_left_cover")
    self.call_service("cover/open_cover", entity_id="cover.sleep_blinds_right_cover")
