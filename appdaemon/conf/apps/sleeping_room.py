from datetime import datetime, timedelta
import time
import common
import appdaemon.plugins.hass.hassapi as hass

light_switch_entity = "sensor.sleep_switch_action"
blind_switches = [
  "sensor.sleep_blinds_ctrl_01_action",
  "sensor.sleep_blinds_ctrl_02_action"
]

class SleepingRoomAutomation(hass.Hass):
  def initialize(self):
    self.listen_state(self.on_light_switch_press, light_switch_entity, attribute="action")
    self.listen_state(self.on_switch_triggered, blind_switches, attribute="action")

    self.run_daily(self.daily_blind_opening, "04:00:00")
    self.run_daily(self.close_blinds_partially, "sunset + 01:00:00")
    left_state = self.get_state("cover.sleep_blinds_left")
    right_state = self.get_state("cover.sleep_blinds_right")
    self.log(f"Left: {left_state}")
    self.log(f"Right: {right_state}")

  def on_light_switch_press(self, entity, attribute, old, new, kwargs):
    if new != "on":
      return

    common.update_last_action()

    sleep_light = "light.sleep_light"
    if self.get_state(sleep_light) == "on":
      self.turn_off(sleep_light)
    else:
      self.turn_on(sleep_light)

  def on_switch_triggered(self, entity, attribute, old, new, kwargs):
    if new == "close":
      self.close_blinds()
    if new == "open":
      self.open_blinds()

  def open_blinds_partially(self, *args, **kwargs):
    self.call_service("cover/set_cover_position", entity_id="cover.sleep_blinds_left", position=60)
    time.sleep(2)
    self.call_service("cover/open_cover", entity_id="cover.sleep_blinds_right")

  def open_blinds(self, *args, **kwargs):
    self.call_service("cover/open_cover", entity_id="cover.sleep_blinds_left")
    time.sleep(2)
    self.call_service("cover/open_cover", entity_id="cover.sleep_blinds_right")

  def close_blinds_partially(self, *args, **kwargs):
    left_state = self.get_state("cover.sleep_blinds_left")
    right_state = self.get_state("cover.sleep_blinds_right")

    if (left_state == "open"):
      self.call_service("cover/close_cover", entity_id="cover.sleep_blinds_left")
      time.sleep(2)

    if (right_state == "open"):
      self.call_service("cover/set_cover_position", entity_id="cover.sleep_blinds_right", position=78)

  def close_blinds(self, *args, **kwargs):
    self.call_service("cover/close_cover", entity_id="cover.sleep_blinds_right")
    time.sleep(0.5)
    self.call_service("cover/close_cover", entity_id="cover.sleep_blinds_left")

  work_day_factor = 1.2
  weekend_factor = 1.3
  def daily_blind_opening(self, *args, **kwargs):
    today = self.date()
    today_is_workday = today.weekday() < 5

    sunrise_today = self.sunrise()
    if sunrise_today.day > today.day:
      # in case we already had sunrise today
      sunrise_today = sunrise_today - timedelta(1)

    # See: https://www.timeanddate.com/sun/germany/leipzig
    min_sunrise = datetime(today.year, today.month, today.day, 4, 53)
    max_sunrise = datetime(today.year, today.month, today.day, 8, 15)

    avg_work_day_wakeup_time = datetime(today.year, today.month, today.day, 6, 45)
    avg_weekend_wakeup_time = datetime(today.year, today.month, today.day, 8, 45)

    work_day_wakeup_time = sunrise_today + (avg_work_day_wakeup_time - sunrise_today) / self.work_day_factor
    weekend_wakeup_time = sunrise_today + (avg_weekend_wakeup_time - sunrise_today) / self.weekend_factor

    self.log(f'Sunrise: min={min_sunrise} today={sunrise_today} max={max_sunrise}')

    self.log(f'Work day min (summer): {(min_sunrise + (avg_work_day_wakeup_time - min_sunrise) / self.work_day_factor).time()}')
    self.log(f'Work day now:          {work_day_wakeup_time.time()}')
    self.log(f'Work day max (winter): {(max_sunrise + (avg_work_day_wakeup_time - max_sunrise) / self.work_day_factor).time()}\n')

    self.log(f'Weekend min (summer):  {(min_sunrise + (avg_weekend_wakeup_time - min_sunrise) / self.weekend_factor).time()}')
    self.log(f'Weekend now:           {weekend_wakeup_time.time()}')
    self.log(f'Weekend max (winter):  {(max_sunrise + (avg_weekend_wakeup_time - max_sunrise) / self.weekend_factor).time()}\n')

    if today_is_workday:
      self.run_at(self.open_blinds, work_day_wakeup_time)
    else:
      self.run_at(self.open_blinds_partially, weekend_wakeup_time)
