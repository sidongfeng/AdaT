import subprocess
import time

import re

class APK():
    """ An abstract class to handle apk.
    """
    def __init__(self, apk_path):
        super(APK, self).__init__()
        self.apk_path = apk_path
        self.apk_name = None
    
    def install(self):
        start_time = time.time()
        commands = ['adb', 'install', '-d', self.apk_path]
        result = subprocess.run(commands, 
                                stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8')
        
        total_time = time.time() - start_time
        if 'Success' in result:
            self.apk_name = self.find_name()
            print(f'>>> {self.apk_name} is Successfully installed, Time elapsed {total_time}s')
            return True
        elif 'INSTALL_FAILED_ALREADY_EXISTS' in result:
            self.apk_name = self.find_name()
            print(f'>>> {self.apk_name} is Successfully installed, Time elapsed {total_time}s')
            return True
        else:
            print(f'>>> Apk File does not install')
            return False

    def find_name(self):
        commands = ['aapt', 'dump', 'badging', self.apk_path, '|', 
                        'findstr', '-n', '"package: name"', '|', 
                        'findstr', '"1:"']
        result = subprocess.run(commands, 
                                stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8')
        return re.findall(r"package: name='(.*?)'", result)[0]

    def get_name(self):
        return self.apk_name

    def uninstall(self):
        start_time = time.time()
        if self.apk_name is not None:
            commands = ['adb', 'uninstall', self.apk_name]
            result = subprocess.run(commands, 
                                    stdout=subprocess.PIPE)
            result = result.stdout.decode('utf-8')
            
            total_time = time.time() - start_time
            if 'Success' in result:
                print(f'>>> {self.apk_name} is Successfully uninstalled, Time elapsed {total_time}s')
                return True
            else:
                print(f'>>> {self.apk_name} does not uninstall')
                return False

    def test_monkey(self):
        commands = ['adb', 'shell', 'monkey',
                        '-p', self.apk_name, '--throttle', str(100),
                        '--ignore-crashes', '--ignore-timeouts', '--ignore-security-exceptions', '--ignore-native-crashes',
                        '--monitor-native-crashes', '-v', '-v', '-v', str(100)]
        result = subprocess.run(commands, 
                                stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8')
        print(result)



if __name__ == "__main__":
    apk = APK('tf_apps_output/tf_apps_output_7/com.brentpanther.bitcoinwidget_289.apk')
    apk.install()
    apk.test_monkey()
    apk.uninstall()