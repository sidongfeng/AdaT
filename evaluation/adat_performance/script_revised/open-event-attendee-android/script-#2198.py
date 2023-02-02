# bug reproduction script for bug #2198 of attendee
import os
import sys
import time

import uiautomator2 as u2
import os
import json
trace = {'step': []}

def wait(seconds=2):
    for i in range(0, seconds):
        print("wait 1 second ..")
        time.sleep(1)


if __name__ == '__main__':

    avd_serial = sys.argv[1]
    d = u2.connect(avd_serial)

    d.app_start("com.eventyay.attendee")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "com.eventyay.attendee":
            break
        #d.app_start("org.odk.collect.android")
        time.sleep(2)
    wait()

    coordinate = d(text="Skip").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Skip").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Skip for now").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Skip for now").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(resourceId="com.eventyay.attendee:id/searchFragment").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.eventyay.attendee:id/searchFragment").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Anything").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Anything").click()
    if not out:
        print("SUCCESS")
    wait()

    with open('themis_output/open-event-attendee-android-log-#2198.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
