import subprocess
import time
import os
import re, sys

class APE():
    """ An abstract class to handle ape engine.
    """
    def __init__(self, adb, application, output_dir):
        super(APE, self).__init__()
        self.adb = adb

        self.running_minutes = 1
        self.throttle = 500
        self.device_serial = self.adb.serial
        
        self.apk_name = application.get_name()
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
        commands = ['pull', remote_folder, self.output_dir]
        self.adb.run_cmd(commands)
        print(' >>> Succuessfully pull the result from sdcard')

    def delete_remote_output(self):
        remote_folder = f'/sdcard/sata-{self.apk_name}-ape-sata-running-minutes-{self.running_minutes}'
        commands = ['rm', '-r', remote_folder]
        self.adb.shell(commands)


if __name__ == "__main__":
    None