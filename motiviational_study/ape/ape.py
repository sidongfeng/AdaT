import subprocess
import time
import os
import re, sys

class APE():
    """ An abstract class to handle ape engine.
    """
    def __init__(self, args, apk_name, output_dir):
        super(APE, self).__init__()
        self.running_minutes = int(args.timeout/60)
        self.throttle = int(args.interval*1000)
        if args.device_serial is None:
            devices = []
            commands = ['adb', 'devices']
            result = subprocess.run(commands, 
                                stdout=subprocess.PIPE)
            result = result.stdout.decode('utf-8')
            for line in result.split('\n')[1:]:
                if not line.strip():
                    continue
                if 'offline' in line:
                    continue
                serial, _ = re.split(r'\s+', line, maxsplit=1)
                devices.append(serial)
            self.device_serial = devices[0]
        else:
            self.device_serial = args.device_serial
        
        self.apk_name = apk_name
        self.output_dir = output_dir
    
    def run(self):
        commands = ['adb', '-s', self.device_serial, 'shell', 
                    'CLASSPATH=/data/local/tmp/ape.jar', '/system/bin/app_process',
                    '/data/local/tmp/', 'com.android.commands.monkey.Monkey',
                    '-p', self.apk_name,
                    '--running-minutes', str(self.running_minutes),
                    '--ape', 'sata',
                    '--throttle', str(self.throttle), '>', os.path.join(self.output_dir, 'log.txt')]
        commands = ' '.join(commands)
        os.system(commands)

    def pull_result(self):
        remote_folder = f'/sdcard/sata-{self.apk_name}-ape-sata-running-minutes-{self.running_minutes}'
        commands = ['adb', 'pull', remote_folder, self.output_dir]
        subprocess.run(commands, 
                    stdout=subprocess.PIPE)
        print('>>> Succuessfully pull the result from sdcard')

    def delete_remote_output(self):
        remote_folder = f'/sdcard/sata-{self.apk_name}-ape-sata-running-minutes-{self.running_minutes}'
        commands = ['adb', 'shell', 'rm', '-r', remote_folder]
        subprocess.run(commands, 
                    stdout=subprocess.PIPE)


if __name__ == "__main__":
    None