# bug reproduction script for bug #745 of Omni-Notes
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

    d.app_start("it.feio.android.omninotes.alpha")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "it.feio.android.omninotes.alpha":
            break
        #d.app_start("org.odk.collect.android")
        time.sleep(2)
    wait()

    coordinate = d(resourceId="it.feio.android.omninotes.alpha:id/fab_expand_menu_button").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="it.feio.android.omninotes.alpha:id/fab_expand_menu_button").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(resourceId="it.feio.android.omninotes.alpha:id/fab_note").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="it.feio.android.omninotes.alpha:id/fab_note").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Content").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Content").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(resourceId="it.feio.android.omninotes.alpha:id/menu_attachment").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="it.feio.android.omninotes.alpha:id/menu_attachment").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Camera").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Camera").click()
    if not out:
        print("SUCCESS")
    wait()

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
        print("SUCCESS")
    wait()

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
        print("SUCCESS")
    wait()

    coordinate = d(description="Navigate up").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(description="Navigate up").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(resourceId="it.feio.android.omninotes.alpha:id/root").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="it.feio.android.omninotes.alpha:id/root").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(resourceId="it.feio.android.omninotes.alpha:id/gridview_item_picture").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="it.feio.android.omninotes.alpha:id/gridview_item_picture").click()
    if not out:
        print("SUCCESS")
    wait()

    with open('themis_output/Omni-Notes-log-#745.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
