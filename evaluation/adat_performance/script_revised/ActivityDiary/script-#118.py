# bug reproduction script for bug #118 of ActivityDiary
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
    d.app_start("de.rampro.activitydiary.debug")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "de.rampro.activitydiary.debug":
            break
        time.sleep(2)
    wait()

    # click the Sleeping activity
    coordinate = d(className="android.widget.TextView", text="Sleeping").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.TextView", text="Sleeping").click()
    if not out:
        print("Success: press Sleeping activity")
    wait()

    # click the Sleeping activity
    coordinate = d(className="android.widget.ImageButton", resourceId="de.rampro.activitydiary.debug:id/fab_attach_picture").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.ImageButton", resourceId="de.rampro.activitydiary.debug:id/fab_attach_picture").click()
    if not out:
            print("Success: press Camera")
    wait()

    # click camera button
    coordinate = d(description="Shutter button").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(description="Shutter button").click()
    if not out:
        print("Success: press taking picture")
    wait()

    # click confirm
    coordinate = d(clickable=True)[2].center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(clickable=True)[2].click()
    if not out:
        print("Success: press picture confirmation")
    wait()

    # click the Cinema activity
    coordinate = d(className="android.widget.TextView", text="Cinema").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.TextView", text="Cinema").click()
    if not out:
        print("Success: press Cinema activity")
    wait()

    # click the Navigation
    coordinate = d(className="android.widget.ImageButton", description="Open Navigation").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.ImageButton", description="Open Navigation").click()
    if not out:
        print("Success: press Navigation")
    wait()

    # click the Diary
    coordinate = d(className="android.widget.CheckedTextView", text="Diary").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.CheckedTextView", text="Diary").click()
    if not out:
        print("Success: press Diary")
    wait()

    # long click the image
    coordinate = d(className="android.widget.ImageView",
            resourceId="de.rampro.activitydiary.debug:id/picture").center()
    step = {'action': 'swipe',
                'coordinate_1': coordinate,
                'coordinate_2': coordinate,
                'duration': 1000,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.ImageView",
            resourceId="de.rampro.activitydiary.debug:id/picture").long_click()
    if out:
        print("Success: long click the image")
    wait()

    # click the Okay
    coordinate = d(className="android.widget.Button",
            text="OK").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.Button",
            text="OK").click()
    if not out:
        print("Success: long click the ok")
    wait()

    with open('themis_output/ActivityDiary-log-#118.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
