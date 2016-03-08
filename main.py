# Keyboard tracker gathers high level keyboard usage statistics.
#
# Copyright (C) 2016  Ezekiel Smithburg <tehgeekmeister@gmail.com>
# Copyright (C) 2016  Bjarte Johansen <Bjarte.Johansen@gmail.com>
#
# Based on code from https://gist.github.com/ljos/3019549
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
