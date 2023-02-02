# bug reproduction script for bug #67 of openlauncher
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

    d.app_start("com.benny.openlauncher")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "com.benny.openlauncher":
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

    coordinate_1 = (0, 960)
    coordinate_2 = (540, 960)
    step = {'action': 'swipe',
                'coordinate_1': coordinate_1,
                'coordinate_2': coordinate_2,
                'duration': 1500,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    os.system(f'adb shell input swipe {coordinate_1[0]} {coordinate_1[1]} {coordinate_2[0]} {coordinate_2[1]} 1500')
    # d.swipe(0.0, 0.5, 0.5, 0.5)
    # print("SUCCESS")
    # wait()

    coordinate = d(resourceId="com.benny.openlauncher:id/minBar").child(index="6").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.benny.openlauncher:id/minBar").child(index="6").click()
    if not out:
        print("SUCCESS")
    wait()

    with open('themis_output/openlauncher-log-#67.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
