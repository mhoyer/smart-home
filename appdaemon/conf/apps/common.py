from datetime import datetime

last_action=datetime.now()

def update_last_action():
  global last_action
  last_action=datetime.now()
