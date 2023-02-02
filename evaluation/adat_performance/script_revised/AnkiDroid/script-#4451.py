# bug reproduction script for bug #4451of ankidroid
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
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(description="Navigate up").click()
    if not out:
        print("Success: press navigation")
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
        print("Success: press settings")
    wait()

    coordinate = d(text="Gestures").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Gestures").click()
    if not out:
        print("Success: press gentures")
    wait()

    coordinate = d(resourceId="android:id/checkbox").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="android:id/checkbox").click()
    if not out:
        print("Success: check enable gestures")
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
        print("Success: press navigation")
    wait()

    coordinate = d(text="Reviewing").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Reviewing").click()
    if not out:
        print("Success: press reviewing")
    wait()

    coordinate_1 = d(className="android.widget.ListView").center()
    coordinate_2 = (coordinate_1[0], 195.0)
    os.system(f'adb shell input swipe {coordinate_1[0]} {coordinate_1[1]} {coordinate_2[0]} {coordinate_2[1]} 1500')
    step = {'action': 'swipe',
                'coordinate_1': coordinate_1,
                'coordinate_2': coordinate_2,
                'duration': 1500,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    # out = d(className="android.widget.ListView").swipe("up", steps=10)
    # if not out:
    #     print("Success: scroll down")
    # wait(1)

    coordinate = d(text="Fullscreen mode").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Fullscreen mode").click()
    if not out:
        print("Success: press full screen mode")
    wait()

    coordinate = d(text="Hide the system bars and answer buttons").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Hide the system bars and answer buttons").click()
    if not out:
        print("Success: press Hide the system bars and answer buttons")
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
        print("Success: press navigation")
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
        print("Success: press navigation")
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

    os.system('adb shell input text "test"')
    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "test"}
    trace['step'].append(step)
    # out = d(className="android.widget.LinearLayout",
    #         resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout") \
    #     .child(className="android.widget.RelativeLayout", index="1") \
    #     .child(resourceId="com.ichi2.anki:id/id_note_editText").set_text("test")
    # if out:
    #     print("Success: set front text")
    # wait()

    os.system('adb shell input text "test"')
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
    # if out:
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

    with open('themis_output/AnkiDroid-log-#4451.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
