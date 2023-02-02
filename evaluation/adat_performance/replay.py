import tqdm
import glob
import os
import time
import argparse

from apk import APK
from device import Device
from adapter import ADB
from seed_trace import SeedTouchTrace, SeedThemisTrace
from rendering_classifier import Classifer
from minicap import Minicap


def get_args(description='Experiment for Performance of AdaT'):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--seed_dir', type=str, required=True,
                        help='Seed instrument of touch position')
    parser.add_argument('--replay_mode', type=str, default='touch',
                        help='Replay mode for script. [touch, themis]')
    parser.add_argument('--themis_dir', type=str, required=True, help='directory of apk data')
    parser.add_argument('--device_serial', type=str, required=True, help='emulator device serial')
    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the log will be written.")
    parser.add_argument('--throttle', type=int, default=1000, help='interval between events in milliseconds')

    parser.add_argument("--init_model", type=str, default='../../approach/GUI_classification/output/mobilenet/pytorch_model.bin.20',
                        help="binary classifer model path")
    parser.add_argument("--model_name", type=str, default='mobilenet', help="name of the binary classifer model")
    parser.add_argument("--max_model_tries", type=int, default=4, help="maximum tries for binary classifer prediction.")
    parser.add_argument("--use_classifer", action="store_true", help="Declare whether use binary classifer to throttle event.")
    parser.add_argument("--use_minicap", action="store_true", help="Declare whether use minicap.")
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    writer = open(os.path.join(args.output_dir, 'log.log'), 'w')
    for key in sorted(args.__dict__):
        writer.write("  <<< {}: {} \n".format(key, args.__dict__[key]))
    writer.close()

    classifer = None
    if args.use_classifer:
        classifer = Classifer(args.init_model, args.model_name)
        classifer.model_warmup()

    minicap = None
    adb = ADB(args.device_serial)
    device = Device(adb)
    if args.use_minicap:
        minicap = Minicap(device)
        minicap.set_up()
        minicap.connect()
        time.sleep(1)

    for script in tqdm.tqdm(glob.glob(os.path.join(args.seed_dir, '*.json'))):
        app_name = script.split('/')[-1].split('-log')[0]
        tag = script.split('#')[-1].split('.json')[0]
        apk_path = glob.glob(os.path.join(args.themis_dir, app_name, f'*{tag}*.apk'))[0]
        app_replay_output = os.path.join(args.output_dir, f'{app_name}_#{tag}')

        os.mkdir(app_replay_output)

        # init device and minicap
        device = Device(adb, app_replay_output)
        if minicap is not None:
            minicap.update_device(device)

        # install apk and grant all premission
        application = APK(apk_path, adb)
        is_installed = application.install()
        if not is_installed:
            print(f' <<< FAILURE APK INSTALLED')
            continue
        application.grant_premission()
        application.launch()
        time.sleep(1)
        
        # replay script
        if args.replay_mode == 'touch':
            STT = SeedTouchTrace(adb, application, device, script, args.throttle, 
                                    classifer, args.max_model_tries, minicap=None)
            start_time = time.time()
            number_of_traces = STT.replay_script()
            time_spent = time.time() - start_time
            print(f' >>> Time Spent {time_spent} s to replay {number_of_traces} steps')
            with open(os.path.join(app_replay_output, 'log.txt'), 'w') as writer:
                writer.write(f' >>> Time Spent:{time_spent}\n')
                writer.write(f' >>> Steps:{number_of_traces}')
        elif args.replay_mode == 'themis':
            python_script = os.path.join('script_revised', app_name, f'script-#{tag}.py')
            STT = SeedThemisTrace(device, python_script)
            start_time = time.time()
            STT.replay_script()
            time_spent = time.time() - start_time
            print(f' >>> Time Spent {time_spent} s')
            with open(os.path.join(app_replay_output, 'log.txt'), 'w') as writer:
                writer.write(f' >>> Time Spent:{time_spent}\n')

        # uninstall app and go to home page
        application.uninstall()
        adb.shell('input keyevent 3'.split())
        time.sleep(2)

    if minicap is not None:
        minicap.disconnect()
        minicap.tear_down()
    
if __name__ == "__main__":
    main()