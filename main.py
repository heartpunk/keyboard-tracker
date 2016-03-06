# cocoa_keypress_monitor.py by Bjarte Johansen is licensed under a 
# License: http://ljos.mit-license.org/

import datetime
import os
import sqlite3

from AppKit import NSApplication, NSApp
from Foundation import NSObject, NSLog
from Cocoa import NSEvent, NSKeyDownMask
from PyObjCTools import AppHelper



conn = sqlite3.connect(os.path.expanduser('~/.keyboard-tracker/something.db'))

schema = """
CREATE TABLE keypresses(
  characters varchar(10),
  characters_ignoring_modifiers varchar(10),
  keycode integer,
  modifier_flags integer,
  timestamp_since_boot double,
  timestamp text
);
"""

insert = "insert into keypresses values(?, ?, ?, ?, ?, ?);"

cursor = conn.cursor()

try:
    cursor.execute(schema)
except:
    pass

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        mask = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, handler)

def handler(event):
    try:
        event_data = [
            event._.characters,                  # unicode
            event._.charactersIgnoringModifiers, # unicode
            event._.keyCode,                     # integer (could probably be small, but who cares)
            event._.modifierFlags,               # integer
            event._.timestamp,                   # double
            datetime.datetime.now(),                      # timestamp
        ]

        cursor.execute(insert, event_data)
        conn.commit()
        print(event_data)
    except KeyboardInterrupt:
        AppHelper.stopEventLoop()

def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()

if __name__ == '__main__':
    main()
