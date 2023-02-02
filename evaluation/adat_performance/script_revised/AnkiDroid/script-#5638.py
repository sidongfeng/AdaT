# bug reproduction script for bug #5638 of ankidroid
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

    coordinate = d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").click()
    if not out:
        print("Success: press fab button")
    wait()

    coordinate = d(resourceId="com.ichi2.anki:id/add_note_action").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.ichi2.anki:id/add_note_action").click()
    if not out:
        print("Success: press add")
    wait()

    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "\\&bsol\\;"}
    trace['step'].append(step)
    out = d(className="android.widget.LinearLayout",
            resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout") \
        .child(className="android.widget.RelativeLayout", index="1") \
        .child(resourceId="com.ichi2.anki:id/id_note_editText").set_text("&bsol;")
    if not out:
        print("Success: set front text")
    wait()

    with open('themis_output/AnkiDroid-log-#5638.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
