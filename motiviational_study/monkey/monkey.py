import subprocess
import time
import os
import re, sys
import threading
import _thread as thread

class Monkey():
    """ An abstract class to handle monkey engine.
    """
    def __init__(self, args, apk_name, output_dir):
        super(Monkey, self).__init__()
        self.runtime = int(args.timeout)
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
        try:
            @exit_after(self.runtime)
            def monkey_test():
                commands = f"adb -s {self.device_serial} shell monkey -p {self.apk_name} --throttle {self.throttle} --ignore-crashes --ignore-timeouts --ignore-security-exceptions -v -v -v 99999999999 > log.txt"
                os.system(commands)
            monkey_test()
        except KeyboardInterrupt:
            print(f'Timeout {self.runtime} s')
            pass
        


def quit_function(fn_name):
    thread.interrupt_main() # raises KeyboardInterrupt

def exit_after(s):
    '''
    use as decorator to exit process if 
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer

if __name__ == "__main__":
    None