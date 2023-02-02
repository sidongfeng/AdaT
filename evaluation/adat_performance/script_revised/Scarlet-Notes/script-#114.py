# bug reproduction script for bug #114 of Scarlet-Notes
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

    d.app_start("com.bijoysingh.quicknote")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "com.bijoysingh.quicknote":
            break
        #d.app_start("org.odk.collect.android")
        time.sleep(2)
    wait()

    coordinate = d(resourceId="com.bijoysingh.quicknote:id/lithoBottomToolbar").child(index="0").child(index="1").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.bijoysingh.quicknote:id/lithoBottomToolbar").child(index="0").child(index="1").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Add Notebook").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "myBook"}
    trace['step'].append(step)
    out = d(text="Add Notebook").set_text("myBook")
    if out:
        print("SUCCESS")
    wait()

    step = {'action': 'keyevent',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': '66',
                'text': None}
    trace['step'].append(step)
    d.press("enter")
    print("SUCCESS")
    wait()

    coordinate = d(text="myBook").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="myBook").click()
    if out:
        print("SUCCESS")
    wait()


    coordinate = d(resourceId="com.bijoysingh.quicknote:id/lithoBottomToolbar", index="2").child(index="0").child(index="3").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.bijoysingh.quicknote:id/lithoBottomToolbar", index="2").child(index="0").child(index="3").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Add Heading…").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "Note1"}
    trace['step'].append(step)
    out = d(text="Add Heading…").set_text("Note1")
    if out:
        print("SUCCESS")
    wait()

    step = {'action': 'keyevent',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': '4',
                'text': None}
    trace['step'].append(step)
    d.press("back")
    print("SUCCESS")
    wait()

    step = {'action': 'keyevent',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': '4',
                'text': None}
    trace['step'].append(step)
    d.press("back")
    print("SUCCESS")
    wait()
    
    coordinate = d(text="myBook").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="myBook").click()
    if out:
        print("SUCCESS")
    wait()

    coordinate = d(resourceId="com.bijoysingh.quicknote:id/lithoBottomToolbar", index="2").child(index="0").child(index="3").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.bijoysingh.quicknote:id/lithoBottomToolbar", index="2").child(index="0").child(index="3").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Add Heading…").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "Note2"}
    trace['step'].append(step)
    out = d(text="Add Heading…").set_text("Note2")
    if out:
        print("SUCCESS")
    wait()

    step = {'action': 'keyevent',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': '4',
                'text': None}
    trace['step'].append(step)
    d.press("back")
    print("SUCCESS")
    wait()

    step = {'action': 'keyevent',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': '4',
                'text': None}
    trace['step'].append(step)
    d.press("back")
    print("SUCCESS")
    wait()

    coordinate = d(text="myBook").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="myBook").click()
    if out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Note1").center()
    step = {'action': 'swipe',
                'coordinate_1': coordinate,
                'coordinate_2': coordinate,
                'duration': 1000,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    os.system('adb shell input swipe 810 292 810 292 1000')
    # out = d(text="Note1").long_click()
    # if out:
    #     print("SUCCESS")
    # wait()

    coordinate = d(text="Lock Note").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Lock Note").click()
    if not out:
        print("SUCCESS")
    wait()
    
    coordinate = d(resourceId="com.bijoysingh.quicknote:id/lithoBottomToolbar", index="2").child(index="0").child(index="0").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.bijoysingh.quicknote:id/lithoBottomToolbar", index="2").child(index="0").child(index="0").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(text="Locked").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(text="Locked").click()
    if not out:
        print("SUCCESS")
    wait()

    coordinate = d(resourceId="com.bijoysingh.quicknote:id/lithoPreBottomToolbar", index="1").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(resourceId="com.bijoysingh.quicknote:id/lithoPreBottomToolbar", index="1").click(offset=(0.05, 0.5))
    if not out:
        print("SUCCESS")
    wait()

    with open('themis_output/Scarlet-Notes-log-#114.json', 'w') as writer:
        writer.write(json.dumps(trace))


    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
