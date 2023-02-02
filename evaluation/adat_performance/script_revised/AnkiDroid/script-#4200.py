# bug reproduction script for bug #4200 of ankidroid
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

def enAbleDontKeepA(d):
    d.press("home")
    wait()

    out = d(resourceId="com.android.launcher3:id/layout").child(index="1").child(index="2").click()
    if not out:
        print("SUCCESS")
    wait()

    out = d(text="Search Apps…").set_text("Settings")
    if out:
        print("SUCCESS")
    wait()

    out = d(resourceId="com.android.launcher3:id/icon", text="Settings").click()
    if not out:
        print("SUCCESS")
    wait()

    out = d(description="Search settings").click()
    if not out:
        print("SUCCESS")
    wait()

    out = d(text="Search…").set_text("keep activities")
    if out:
        print("SUCCESS")
    wait()

    out = d(text="Don’t keep activities").click()
    if not out:
        print("SUCCESS")
    wait()

    out = d(text="Don’t keep activities").click()
    if not out:
        print("SUCCESS")
    wait()

if __name__ == '__main__':

    avd_serial = sys.argv[1]
    d = u2.connect(avd_serial)

    # enAbleDontKeepA(d)

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

    coordinate = d(className="android.widget.LinearLayout",
            resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout")\
        .child(className="android.widget.RelativeLayout", index="1")\
        .child(resourceId="com.ichi2.anki:id/id_note_editText").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.LinearLayout",
            resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout")\
        .child(className="android.widget.RelativeLayout", index="1")\
        .child(resourceId="com.ichi2.anki:id/id_note_editText").click()
    if not out:
        print("Success: click front text")
    wait()

    os.system('adb shell input text "test"')
    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "test"}
    trace['step'].append(step)
    # out = d(className="android.widget.LinearLayout",
    #         resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout")\
    #     .child(className="android.widget.RelativeLayout", index="1")\
    #     .child(resourceId="com.ichi2.anki:id/id_note_editText").set_text("test")
    # if not out:
    #     print("Success: set front text")
    # wait()

    
    coordinate = d(resourceId="com.ichi2.anki:id/action_save").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.ichi2.anki:id/action_save").click()
    if not out:
        print("Success: press save")
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
        print("Success: press back")
    wait()

    coordinate = d(text="Default").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Default").click()
    if not out:
        print("Success: press default")
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

    coordinate = d(text="Edit note").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Edit note").click()
    if not out:
        print("Success: press Edit Note")
    wait()

    coordinate = d(className="android.widget.LinearLayout",
            resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout") \
        .child(className="android.widget.RelativeLayout", index="3") \
        .child(resourceId="com.ichi2.anki:id/id_note_editText").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.LinearLayout",
            resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout") \
        .child(className="android.widget.RelativeLayout", index="3") \
        .child(resourceId="com.ichi2.anki:id/id_note_editText").click()
    if not out:
        print("Success: click front text")
    wait()

    os.system('adb shell input text "you"')
    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "you"}
    trace['step'].append(step)
    # out = d(className="android.widget.LinearLayout",
    #         resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout") \
    #     .child(className="android.widget.RelativeLayout", index="3") \
    #     .child(resourceId="com.ichi2.anki:id/id_note_editText").set_text("you")
    # if not out:
    #     print("Success: set back text")
    # wait()

    coordinate = d(resourceId="com.ichi2.anki:id/action_save").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.ichi2.anki:id/action_save").click()
    if not out:
        print("Success: press save")
    wait()

    with open('themis_output/AnkiDroid-log-#4200.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
