import subprocess
import time
import os
import re, sys

class FastBot():
    """ An abstract class to handle fastbot engine.
    """
    def __init__(self, adb, application=None, output_dir=None):
        super(FastBot, self).__init__()
        self.adb = adb

        self.running_minutes = 1
        self.throttle = 500
        self.device_serial = self.adb.serial
        
        self.apk_name = None
        if application is not None:
            self.apk_name = application.get_name()
        self.output_dir = output_dir
    
    def setup(self):
        push_framework_command = f'push {self.local_resource_dir}/framework.jar /sdcard'
        push_fastbot_command = f'push {self.local_resource_dir}/fastbot-thirdpart.jar /sdcard'
        push_monkey_command = f'push {self.local_resource_dir}/monkeyq.jar /sdcard'
        self.adb.run_cmd(push_framework_command.split())
        self.adb.run_cmd(push_fastbot_command.split())
        self.adb.run_cmd(push_monkey_command.split())
        
        abi = self.adb.get_property('ro.product.cpu.abi')
        push_libs_command = f'push {self.local_resource_dir}/libs/{abi} /data/local/tmp/'
        self.adb.run_cmd(push_libs_command.split())
    
    def setup_screenshot(self):
        push_config_command = f'push {self.local_resource_dir}/max.config /sdcard'
        self.adb.run_cmd(push_config_command.split())

    def run(self):
        commands = ['adb', '-s', self.device_serial, 'shell', 
                    'CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar',
                    'exec', 'app_process', '/system/bin', 'com.android.commands.monkey.Monkey',
                    '-p', self.apk_name, '--agent', 'reuseq',
                    '--running-minutes', str(self.running_minutes),
                    '--throttle', str(self.throttle), '-v', '-v', '>', os.path.join(self.output_dir, 'log.txt')]
        commands = ' '.join(commands)
        os.system(commands)

    def pull_result(self):
        remote_folder = f'/sdcard/fastbot-{self.apk_name}--running-minutes-{self.running_minutes}'
        commands = ['pull', remote_folder, self.output_dir]
        self.adb.run_cmd(commands)
        print(' >>> Succuessfully pull the result from sdcard')

    def delete_remote_output(self):
        remote_folder = f'/sdcard/fastbot-{self.apk_name}--running-minutes-{self.running_minutes}'
        commands = ['rm', '-r', remote_folder]
        self.adb.shell(commands)

    def disconnect(self):
        framework_command = 'rm /sdcard/framework.jar'
        fastbot_command = 'rm /sdcard/fastbot-thirdpart.jar'
        monkey_command = 'rm /sdcard/monkeyq.jar'
        self.adb.shell(framework_command.split())
        self.adb.shell(fastbot_command.split())
        self.adb.shell(monkey_command.split())
        
        abi = self.adb.get_property('ro.product.cpu.abi')
        libs_command = f'rm -r /data/local/tmp/{abi}'
        self.adb.shell(libs_command.split())

        config_command = 'rm /sdcard/max.config'
        self.adb.shell(config_command.split())

if __name__ == "__main__":
    None