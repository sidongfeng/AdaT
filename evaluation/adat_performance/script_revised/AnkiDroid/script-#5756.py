# bug reproduction script for bug #5756 of ankidroid
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
    out = d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").click()
    if not out:
        print("Success: press fab button")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(resourceId="com.ichi2.anki:id/add_note_action").center()
    out = d(resourceId="com.ichi2.anki:id/add_note_action").click()
    if not out:
        print("Success: press add")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    # out = d(className="android.widget.LinearLayout",
    #         resourceId="com.ichi2.anki:id/CardEditorEditFieldsLayout") \
    #     .child(className="android.widget.RelativeLayout", index="1") \
    #     .child(resourceId="com.ichi2.anki:id/id_note_editText").set_text("aaa")
    # if not out:
    #     print("Success: set front text")
    # wait()
    os.system('adb shell input text "aaa"')
    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "aaa"}
    trace['step'].append(step)

    coordinate = d(resourceId="com.ichi2.anki:id/action_save").center()
    out = d(resourceId="com.ichi2.anki:id/action_save").click()
    if not out:
        print("Success: press save")
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
        print("Success: press back")
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

    coordinate = d(text="Create filtered deck").center()
    out = d(text="Create filtered deck").click()
    if not out:
        print("Success: press Create filtered deck")
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
        print("Success: press CREATE")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="cards selected by").center()
    out = d(text="cards selected by").click()
    if not out:
        print("Success: press cards selected by")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Random").center()
    out = d(text="Random").click()
    if not out:
        print("Success: Random")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="cards selected by").center()
    out = d(text="cards selected by").click()
    if not out:
        print("Success: press cards selected by")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Oldest seen first").center()
    out = d(text="Oldest seen first").click()
    if not out:
        print("Success: Oldest seen first")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    x, y = d(description="Navigate up").center()
    d.double_click(x, y, duration=0.5)
    if not out:
        print("Success: press back")
    wait()
    step = {'action': 'double_tap',
                'coordinate_1': (x, y),
                'coordinate_2': None,
                'duration': 0.5,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(description="", resourceId="", className="android.widget.ImageButton").center()
    out = d(description="", resourceId="", className="android.widget.ImageButton").click()
    if not out:
        print("Success: press back")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    coordinate = d(text="Filtered Deck 1").center()
    out = d(text="Filtered Deck 1").click()
    if not out:
        print("Success: Filtered Deck 1")
    wait()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)

    with open('themis_output/AnkiDroid-log-#5756.json', 'w') as writer:
        writer.write(json.dumps(trace))

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
