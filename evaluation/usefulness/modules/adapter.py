import subprocess
import re

class ADB(object):
    def __init__(self, serial=None):
        self.serial = serial
        if serial is None:
            self.serial = self.find_devices[0]
    
    def find_devices(self):
        devices = []
        result = subprocess.run(['adb', 'devices'], 
                    stdout=subprocess.PIPE).stdout.decode('utf-8')
        for line in result.split('\n')[1:]:
            if not line.strip() or 'offline' in line:
                continue
            serial, _ = re.split(r'\s+', line, maxsplit=1)
            devices.append(serial)
        return devices

    def run_cmd(self, extra_args):
        if isinstance(extra_args, str):
            extra_args = extra_args.split(' ')
        args = ['adb', '-s', self.serial] + extra_args
        # print(' >>> {}'.format(' '.join(args)))
        result = subprocess.run(args, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def shell(self, extra_args):
        if isinstance(extra_args, str):
            extra_args = extra_args.split(' ')
        args = ['adb', '-s', self.serial, 'shell'] + extra_args
        # print(' >>> {}'.format(' '.join(args)))
        result = subprocess.run(args, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def get_property(self, property_name):
        """
        get the value of property
        @param property_name:
        @return:
        """
        return self.shell(["getprop", property_name]).strip()
    
    def get_sdk_version(self):
        """
        Get version of SDK, e.g. 18, 20
        """
        VERSION_SDK_PROPERTY = 'ro.build.version.sdk'
        return int(self.get_property(VERSION_SDK_PROPERTY))
    