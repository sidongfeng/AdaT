import random
import numpy as np
import time
import argparse
import cv2
from PIL import Image
import os

from apk import APK
from device import Device
from adapter import ADB
from rendering_classifier import Classifer
from minicap import Minicap


def get_args(description='Experiment for Performance of Throttledroid'):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--apk', type=str, required=True,
                        help='App under test')
    parser.add_argument('--device_serial', type=str, required=True, help='emulator device serial')

    parser.add_argument("--output_dir", default=None, type=str,
                        help="The output directory where the log will be written.")
    parser.add_argument("--init_model", type=str, default='../GUI_classification/output/mobilenet/pytorch_model.bin.20',
                        help="binary classifer model path")
    parser.add_argument("--model_name", type=str, default='mobilenet', help="name of the binary classifer model")
    parser.add_argument("--max_model_tries", type=int, default=4, help="maximum tries for binary classifer prediction.")
    parser.add_argument("--max_throttle", type=int, default=1000, help="maximum throttle interval for binary classifer prediction.")
    args = parser.parse_args()

    return args


def main():
    args = get_args()

    # init classifier
    classifer = Classifer(args.init_model, args.model_name)
    classifer.model_warmup()

    # init device and minicap
    minicap = None
    adb = ADB(args.device_serial)
    device = Device(adb)
    minicap = Minicap(device)
    minicap.set_up()
    minicap.connect()
    time.sleep(1)

    # install apk and grant all premission
    apk_path = args.apk
    application = APK(apk_path, adb)
    is_installed = application.install()
    if not is_installed:
        print(f' <<< FAILURE APK INSTALLED')
        if minicap is not None:
            minicap.disconnect()
            minicap.tear_down()
        exit()
    application.grant_premission()
    application.launch()
    time.sleep(1)

    start_time = time.time()
    time_spent = time.time() - start_time
    # send random tap event for 1 minute runtime
    while time_spent < 60:
        random_x = random.randint(0, device.get_width())
        random_y = random.randint(0, device.get_height())
        adb.shell(f'input tap {random_x} {random_y}')

        # GUI rendering state classification
        rendering_time = time.time()
        is_blurred = True
        predict_tries = 0
        image_storage = []
        while is_blurred and \
                predict_tries < args.max_model_tries and \
                time.time()-rendering_time < args.max_throttle/1000:
            predict_tries += 1
            
            last_know_screenshot = minicap.last_screen
            last_know_tag = minicap.last_screen_time
            last_know_screenshot = np.array(bytearray(last_know_screenshot))
            last_know_screenshot = cv2.imdecode(last_know_screenshot, 1)
            last_know_screenshot_pil = Image.fromarray(last_know_screenshot)

            is_blurred = classifer.predict_img(last_know_screenshot_pil)
            image_storage.append((last_know_tag, last_know_screenshot))
        
        # save images for minicap
        if args.output_dir is not None:
            img_save_path = f'screen_{image_storage[-1][0]}.png'
            local_image_path = os.path.join(args.output_dir, img_save_path)
            cv2.imwrite(local_image_path, image_storage[-1][1])

        time_spent = time.time() - start_time


    # uninstall app and disconnect minicap
    application.uninstall()
    if minicap is not None:
        minicap.disconnect()
        minicap.tear_down()
    
if __name__ == "__main__":
    main()
