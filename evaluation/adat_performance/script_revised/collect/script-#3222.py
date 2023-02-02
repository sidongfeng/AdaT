# bug reproduction script for bug #3222 of collect
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

    step = {'action': 'before',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': "adb root && adb shell am start -n org.odk.collect.android/org.odk.collect.android.activities.MainMenuActivity",
                'text': None}
    trace['step'].append(step)
    os.system("adb root && adb shell am start -n org.odk.collect.android/org.odk.collect.android.activities.MainMenuActivity")
    #d.app_start("org.odk.collect.android")
    #d.shell("am start -n org.odk.collect.android/org.odk.collect.android.activities.MainMenuActivity")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "org.odk.collect.android":
            break
        #d.app_start("org.odk.collect.android")
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

    coordinate = d(text="General Settings").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="General Settings").click()
    if not out:
        print("Success: press General Settings")
    wait()

    coordinate = d(text="Form management").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Form management").click()
    if not out:
        print("Success: press Form management")
    wait()

    coordinate = d(text="Hide old form versions").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Hide old form versions").click()
    if not out:
        print("Success: press Hide old form versions")
    wait()

    step = {'action': 'keyevent',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': '4',
                'text': None}
    trace['step'].append(step)
    step = {'action': 'keyevent',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': '4',
                'text': None}
    trace['step'].append(step)
    # d.press("back")
    # d.press("back")
    os.system('adb shell input keyevent 4')
    os.system('adb shell input keyevent 4')
    print("Success: doulbe back")

    coordinate = d(text="Fill Blank Form").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Fill Blank Form").click()
    if not out:
        print("Success: press Fill Blank Form")
    wait()

    with open('themis_output/collect-log-#3222.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
