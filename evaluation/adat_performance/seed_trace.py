import json
import time
from datetime import datetime
import os
import numpy as np
import cv2
from PIL import Image

from event import Event

class SeedTouchTrace():
    def __init__(self, adb, application, device, script, throttle, classifer, max_model_tries, minicap):
        self.adb = adb
        self.application = application
        self.device = device

        self.script = script
        self.throttle = throttle
        self.classifer = classifer
        self.max_model_tries = max_model_tries
        self.minicap = minicap

    def read_script(self):
        with open(self.script) as json_file:
            traces = json.loads(json_file.read())
        return traces
    
    def run_event(self, event, action):
        if action == 'tap':
            event.tap()
        elif action == 'swipe':
            event.swipe()
        elif action == 'intent':
            event.intent()
        elif action == 'text':
            event.input_text()
        elif action == 'double_tap':
            event.double_tap()
        elif action == 'keyevent':
            event.send_keyevent()
        elif action == 'before':
            event.before_launch()
            self.application.launch()
        else:
            print(f' >>> Wrong action {action}')

    def replay_script(self):
        traces = self.read_script()

        for step in traces['step']:
            action = step['action']
            coord_1 = step['coordinate_1']
            coord_2 = step['coordinate_2']
            duration = step['duration']
            commands = step['commands']
            text = step['text']

            event = Event(self.adb, action, coord_1, coord_2, duration, commands, text)
            self.run_event(event, action)

            if self.classifer is None:
                time.sleep(self.throttle/1000)
                self.take_screenshot()
            else:
                start_time = time.time()
                is_blurred = True
                predict_tries = 0
                image_path_storage = set()
                image_storage = []
                while is_blurred and \
                        predict_tries < self.max_model_tries and \
                        time.time()-start_time < self.throttle/1000:
                    
                    predict_tries += 1
                    if self.minicap is None:
                        local_image_path = self.take_screenshot()
                        is_blurred = self.classifer.predict_img_path(local_image_path)
                        image_path_storage.add(local_image_path)
                    else:
                        last_know_screenshot = self.minicap.last_screen
                        last_know_tag = self.minicap.last_screen_time
                        last_know_screenshot = np.array(bytearray(last_know_screenshot))
                        last_know_screenshot = cv2.imdecode(last_know_screenshot, 1)
                        last_know_screenshot_pil = Image.fromarray(last_know_screenshot)
                        # if last_know_screenshot is None:
                        #     print(' <<< Error image from minicap')
                        #     break
                        is_blurred = self.classifer.predict_img(last_know_screenshot_pil)
                        image_storage.append((last_know_tag, last_know_screenshot))
                        
                # remove blurred images for adb capture
                if len(image_path_storage) > 1:
                    for img_path in sorted(image_path_storage)[:-1]:
                        os.remove(img_path)
                
                # save images for minicap
                if len(image_storage) > 0:
                    img_save_path = f'screen_{image_storage[-1][0]}.png'
                    local_image_path = os.path.join(self.device.output_dir, img_save_path)
                    cv2.imwrite(local_image_path, image_storage[-1][1])
        
        return len(traces['step'])
    
    def take_screenshot(self):
        tag = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return self.device.take_screenshot(f'screen_{tag}.png')


class SeedThemisTrace():
    def __init__(self, device, script):
        self.device = device
        self.script = script

    def replay_script(self):
        print(f"python {self.script} {self.device.adb.serial}")
        os.system(f"python {self.script} {self.device.adb.serial}")
        self.take_screenshot()
    
    def take_screenshot(self):
        tag = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return self.device.take_screenshot(f'screen_{tag}.png')