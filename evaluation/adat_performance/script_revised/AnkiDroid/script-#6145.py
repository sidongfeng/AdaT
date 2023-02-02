# bug reproduction script for bug #6145 of ankidroid
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

    d.app_start("com.ichi2.anki")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "com.ichi2.anki":
            break
        time.sleep(2)
    wait()

    
    coordinate = d(description="Navigate up").center()
    out = d(description="Navigate up").click()
    if not out:
        print("Success: press navigation")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Settings").center()
    out = d(text="Settings").click()
    if not out:
        print("Success: press settings")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="AnkiDroid").center()
    out = d(text="AnkiDroid").click()
    if not out:
        print("Success: press AnkiDroid")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate_1 = d(className="android.widget.ListView").center()
    coordinate_2 = (coordinate_1[0], 195.0)    
    os.system(f'adb shell input swipe {coordinate_1[0]} {coordinate_1[1]} {coordinate_2[0]} {coordinate_2[1]} 1500')
    # out = d(className="android.widget.ListView").swipe("up", steps=10)
    # if not out:
    #     print("Success: scroll down")
    # wait(1)
    step = {'action': 'swipe',
                'coordinate_1': coordinate_1,
                'coordinate_2': coordinate_2,
                'duration': 1500,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Language").center()
    out = d(text="Language").click()
    if not out:
        print("Success: press Language")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Chinese (China)").center()
    out = d(text="Chinese (China)").click()
    if not out:
        print("Success: press Chinese (China)")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(description="Navigate up").center()
    out = d(description="Navigate up").click()
    if not out:
        print("Success: press navigation")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(description="Navigate up").center()
    out = d(description="Navigate up").click()
    if not out:
        print("Success: press navigation")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Settings").center()
    out = d(text="Settings").click()
    if not out:
        print("Success: press settings")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="高级设置").center()
    out = d(text="高级设置").click()
    if not out:
        print("Success: press 高级设置")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    for x in range(6):
        coordinate_1 = d(className="android.widget.ListView").center()
        coordinate_2 = (coordinate_1[0], 195.0)    
        os.system(f'adb shell input swipe {coordinate_1[0]} {coordinate_1[1]} {coordinate_2[0]} {coordinate_2[1]} 1500')
        # out = d(className="android.widget.ListView").swipe("up", steps=10)
        # if not out:
        #     print("Success: scroll down")
        # wait(1)
        step = {'action': 'swipe',
                'coordinate_1': coordinate_1,
                'coordinate_2': coordinate_2,
                'duration': 1500,
                'commands': None,
                'text': None}
        trace['step'].append(step)

    coordinate = d(text="实验性 V2 调度器").center()
    out = d(text="实验性 V2 调度器").click()
    if not out:
        print("Success: press 实验性 V2 调度器")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="确定").center()
    out = d(text="确定").click()
    if not out:
        print("Success: press 确定")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(description="转到上一层级").center()
    out = d(description="转到上一层级").click()
    if not out:
        print("Success: press navigation")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(description="转到上一层级").center()
    out = d(description="转到上一层级").click()
    if not out:
        print("Success: press navigation")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(description="More options").center()
    out = d(description="More options").click()
    if not out:
        print("Success: press more options")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Export collection").center()
    out = d(text="Export collection").click()
    if not out:
        print("Success: press Export collection")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="OK").center()
    out = d(text="OK").click()
    if not out:
        print("Success: press OK")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    with open('themis_output/AnkiDroid-log-#6145.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
