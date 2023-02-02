# bug reproduction script for bug #285 of ActivityDiary
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


    # click the Navigation
    coordinate = d(className="android.widget.ImageButton", description="Open navigation").center()
    out = d(className="android.widget.ImageButton", description="Open navigation").click()
    if not out:
        print("Success: press Navigation")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)


    # click the Settings
    coordinate = d(className="android.widget.CheckedTextView", text="Settings").center()
    out = d(className="android.widget.CheckedTextView", text="Settings").click()
    if not out:
        print("Success: press Settings")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    # scroll down the settings
    action = 'swipe'
    coordinate_1 = d(className="android.support.v7.widget.RecyclerView", resourceId="de.rampro.activitydiary.debug:id/recycler_view").center()
    coordinate_2 = (coordinate_1[0], 195.0)    
    os.system(f'adb shell input swipe {coordinate_1[0]} {coordinate_1[1]} {coordinate_2[0]} {coordinate_2[1]} 1500')
    # out = d(className="android.support.v7.widget.RecyclerView", resourceId="de.rampro.activitydiary.debug:id/recycler_view").swipe("up")
    # if out:
    #     print("Success: Scroll down")
    # wait()
    step = {'action': 'swipe',
                'coordinate_1': coordinate_1,
                'coordinate_2': coordinate_2,
                'duration': 1500,
                'commands': None,
                'text': None}
    trace['step'].append(step)



    # scroll down the settings
    action = 'swipe'
    coordinate_1 = d(className="android.support.v7.widget.RecyclerView",
            resourceId="de.rampro.activitydiary.debug:id/recycler_view").center()
    coordinate_2 = (coordinate_1[0], 195.0)
    # out = d(className="android.support.v7.widget.RecyclerView",
    #         resourceId="de.rampro.activitydiary.debug:id/recycler_view").swipe("up")
    # if out:
    #     print("Success: scroll down")
    # wait()
    # with open('log-#285.txt', 'a') as writer:
    #     writer.write(f'{coordinate_1} ({coordinate_1[0]}, 194.0) {action}\n')
    os.system(f'adb shell input swipe {coordinate_1[0]} {coordinate_1[1]} {coordinate_2[0]} {coordinate_2[1]} 1500')
    step = {'action': 'swipe',
                'coordinate_1': coordinate_1,
                'coordinate_2': coordinate_2,
                'duration': 1500,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    # click Location Service
    coordinate = d(className="android.widget.TextView", text="Location Service").center()
    out = d(className="android.widget.TextView", text="Location Service").click()
    if not out:
        print("Success: press Location Service")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    # click Network
    coordinate = d(className="android.widget.CheckedTextView", text="Network").center()
    out = d(className="android.widget.CheckedTextView", text="Network").click()
    if not out:
        print("Success: press Network")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    # click Update period
    coordinate = d(className="android.widget.TextView", text="Update period").center()
    out = d(className="android.widget.TextView", text="Update period").click()
    if not out:
        print("Success: press update period")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    # set the edittext to empty
    action = 'text'
    # out = d(className="android.widget.EditText").set_text(text="")
    # if out:
    #     print("Success: set text to empty")
    # wait()
    os.system('adb shell input keyevent KEYCODE_DEL')
    step = {'action': 'intent',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': 'adb shell input keyevent KEYCODE_DEL',
                'text': None}
    trace['step'].append(step)

    # click Ok
    coordinate = d(className="android.widget.Button", text="OK").center()
    out = d(className="android.widget.Button", text="OK").click()
    if not out:
        print("Success: press OK")
    wait()
    step = {'action': 'action',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)


    with open('themis_output/ActivityDiary-log-#285.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
