import glob
import tqdm
import json
import os
import argparse
import subprocess
import time
from apk import APK
from ape import APE

global logger

def get_args(description='Empirical study for APE'):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--apk_folder', type=str, default=None, required=True,
                        help='apk file path')
    parser.add_argument('--timeout', type=int, default=120, help='runtime in seconds')
    parser.add_argument('--interval', type=float, default=2, help="event interval in seconds.")
    parser.add_argument("--d", type=str, default=None, dest="device_serial", required=False,
                        help="The serial number of target device (use `adb devices` to find)")

    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the states and logs will be written.")
    
    args = parser.parse_args()

    for key in sorted(args.__dict__):
        print("  <<< {}: {}".format(key, args.__dict__[key]))
        with open(os.path.join(args.output_dir, 'log.txt'), 'a') as writer:
            writer.write("  <<< {}: {}\n".format(key, args.__dict__[key]))

    num_apks = len(glob.glob(os.path.join(args.apk_folder, '*.apk')))
    print("  <<< {}: {}".format('Num apks', num_apks))
    with open(os.path.join(args.output_dir, 'log.txt'), 'a') as writer:
            writer.write("  <<< {}: {}\n".format('Num apks', num_apks))

    return args

def main():
    global logger
    args = get_args()
    for apk_path in tqdm.tqdm(glob.glob(os.path.join(args.apk_folder, '*.apk'))):
        apk_name = apk_path.split('\\')[-1].replace('.apk', '')
        output_apk_dir = os.path.join(args.output_dir, apk_name)
        os.mkdir(output_apk_dir)
        print('\n\n\n\n>>>  Processing: {}'.format(apk_name))

        apk = APK(apk_path)
        is_installed = apk.install()
        if not is_installed:
            continue

        # execute ape
        ape = APE(args, apk.get_name(), output_apk_dir)
        ape.run()
        ape.pull_result()
        

        apk.uninstall()
        ape.delete_remote_output()
        time.sleep(2)

if __name__ == "__main__":
    main()