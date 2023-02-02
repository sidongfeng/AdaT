# bug reproduction script for bug #1887 of AFM
import sys
import time
import os

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
    d.app_start("com.amaze.filemanager.debug")
    wait()

    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "com.amaze.filemanager.debug":
            break
        time.sleep(2)
    wait()

    coordinate = d(className="android.widget.TextView", resourceId="com.amaze.filemanager.debug:id/search").center()
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    out = d(className="android.widget.TextView", resourceId="com.amaze.filemanager.debug:id/search").click()
    if not out:
        print("Success: press search")
    wait()


    step = {'action': 'text',
                'coordinate_1': None,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': "com"}
    trace['step'].append(step)
    out = d(className="android.widget.EditText", resourceId="com.amaze.filemanager.debug:id/search_edit_text").set_text(text="com")
    if out:
        print("Success: set folder name")
    wait()

    coordinate = (995, 1700)
    step = {'action': 'tap',
                'coordinate_1': coordinate,
                'coordinate_2': None,
                'duration': None,
                'commands': None,
                'text': None}
    trace['step'].append(step)
    os.system('adb shell input tap 995 1700')
    # out = d(className="android.widget.Button", text="SEARCH").click()
    # if not out:
    #     print("Success: press data")
    # wait()

    with open('themis_output/AmazeFileManager-log-#1837.json', 'w') as writer:
        writer.write(json.dumps(trace))


    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
