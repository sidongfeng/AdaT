# bug reproduction script for bug #116 of APhotoManager
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

    d.app_start("de.k3b.android.androFotoFinder")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "de.k3b.android.androFotoFinder":
            break
        time.sleep(2)
    wait()

    coordinate = d(description="More options").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(description="More options").click()
    if not out:
        print("Success: press more options")
    wait()

    coordinate = d(text="Settings").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Settings").click()
    if not out:
        print("Success: press Settings")
    wait()

    with open('themis_output/APhotoManager-log-#116.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
