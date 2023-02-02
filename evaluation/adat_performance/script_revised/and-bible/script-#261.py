# bug reproduction script for bug #261 of andbible
import sys
import time

import uiautomator2 as u2
import os
import json

def wait(seconds=2):
    for i in range(0, seconds):
        print("wait 1 second ..")
        time.sleep(1)


if __name__ == '__main__':

    avd_serial = sys.argv[1]
    d = u2.connect(avd_serial)
    d.app_start("net.bible.android.activity")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "net.bible.android.activity":
            break
        time.sleep(2)
    wait()

    trace = {'step': []}

    coordinate = d(text="OK").center()
    out = d(text="OK").click()
    if not out:
        print("Success: press OK")
    wait(30)
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="AB").center()
    out = d(text="AB").click()
    if not out:
        print("Success: press AB")
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
    wait(10)
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Bible").center()
    out = d(text="Bible").click()
    if not out:
        print("Success: press Bible")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Book").center()
    out = d(text="Book").click()
    if not out:
        print("Success: press Book")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="BaptistConfession1646").center()
    out = d(text="BaptistConfession1646").click()
    if not out:
        print("Success: press BaptistConfession1646")
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
    wait(5)
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

    coordinate = d(className="android.widget.ImageButton", resourceId="net.bible.android.activity:id/homeButton").center()
    out = d(className="android.widget.ImageButton", resourceId="net.bible.android.activity:id/homeButton").click()
    if not out:
        print("Success: press home")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Choose Document").center()
    out = d(text="Choose Document").click()
    if not out:
        print("Success: press Choose Document")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Bible").center()
    out = d(text="Bible").click()
    if not out:
        print("Success: press Bible")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Book").center()
    out = d(text="Book").click()
    if not out:
        print("Success: press Book")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="BaptistConfession1646").center()
    out = d(text="BaptistConfession1646").click()
    if not out:
        print("Success: press BaptistConfession1646")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Confession").center()
    out = d(text="Confession").click()
    if not out:
        print("Success: press Confession")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(className="android.widget.ImageButton", resourceId="net.bible.android.activity:id/homeButton").center()
    out = d(className="android.widget.ImageButton", resourceId="net.bible.android.activity:id/homeButton").click()
    if not out:
        print("Success: press home")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Find").center()
    out = d(text="Find").click()
    if not out:
        print("Success: press Find")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Create").center()
    out = d(text="Create").click()
    if not out:
        print("Success: press Find")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    with open('themis_output/and-bible-log-#261.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
