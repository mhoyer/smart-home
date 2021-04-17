import appdaemon.plugins.hass.hassapi as hass

class WorkRoomAutomation(hass.Hass):

  laser_printer = "switch.work_laser_printer_switch"

  def initialize(self):
    self.run_daily(self.daily_turn_off_laser_printer, "00:00:00")

  def daily_turn_off_laser_printer(self, *args, **kwargs):
    self.log("turning off the printer") 
    self.turn_off(self.laser_printer)
