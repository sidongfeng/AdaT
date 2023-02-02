import subprocess
import time
import os
import re

class APK():
    """ An abstract class to handle apk.
    """
    def __init__(self, apk_path, adb):
        super(APK, self).__init__()
        self.apk_path = apk_path
        self.adb = adb
        self.apk_name = self.find_name()
    
    def install(self):
        commands = f"pm list packages -f".split(' ')
        result = self.adb.shell(commands)
        if self.apk_name in result:
            self.uninstall()

        start_time = time.time()
        commands = ['install', '-d', self.apk_path]
        result = self.adb.run_cmd(commands)
        
        total_time = time.time() - start_time
        if 'Success' in result:
            # print(f'>>> {self.apk_name} is Successfully installed, Time elapsed {total_time}s')
            return True
        elif 'INSTALL_FAILED_ALREADY_EXISTS' in result:
            # print(f'>>> {self.apk_name} is Successfully installed, Time elapsed {total_time}s')
            return True
        else:
            # print(f'>>> Apk File does not install')
            return False
    
    def grant_premission(self):
        string = f"pm grant {self.apk_name} android.permission.READ_EXTERNAL_STORAGE"
        self.adb.shell(string.split(' '))
        string = f"pm grant {self.apk_name} android.permission.WRITE_EXTERNAL_STORAGE"
        self.adb.shell(string.split(' '))
        string = f"pm grant {self.apk_name} android.permission.ACCESS_FINE_LOCATION"
        self.adb.shell(string.split(' '))
        string = f"pm grant {self.apk_name} android.permission.CAMERA"
        self.adb.shell(string.split(' '))
        string = f"pm grant {self.apk_name} android.permission.READ_CONTACTS"
        self.adb.shell(string.split(' '))
        string = f"pm grant {self.apk_name} android.permission.WRITE_CONTACTS"
        self.adb.shell(string.split(' '))

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
            result = self.adb.shell(f'pm uninstall {self.apk_name}'.split( ))
            
            total_time = time.time() - start_time
            if 'Success' in result:
                # print(f'>>> {self.apk_name} is Successfully uninstalled, Time elapsed {total_time}s')
                return True
            else:
                # print(f'>>> {self.apk_name} does not uninstall')
                return False

    def launch(self):
        self.adb.shell(f'monkey -p {self.apk_name} -c android.intent.category.LAUNCHER 1')


if __name__ == "__main__":
    apk = APK('AnkiDroid-debug-2.7beta1-#4451.apk', 'emulator-5554')
    apk.install()
    apk.grant_premission()
    print(apk.get_name())
    # apk.uninstall()