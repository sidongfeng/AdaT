import time
from datetime import datetime
import socket
import subprocess

from device import Device
from adapter import ADB


MINICAP_REMOTE_ADDR = "localabstract:minicap"

class Minicap():
    """
    a connection with target device through minicap.
    """
    def __init__(self, device):
        """
        initiate a minicap connection
        :param device: instance of Device
        :return:
        """
        self.device = device
        self.remote_minicap_path = "/data/local/tmp/minicap-devel"

        self.host = "localhost"
        self.port = self.device.get_random_port()
        self.connected = False
        self.sock = None
        self.minicap_process = None

        self.banner = None

        self.last_screen = None
        self.last_screen_time = None

    def set_up(self):
        adb = self.device.adb

        try:
            minicap_files = adb.shell("ls %s 2>/dev/null" % self.remote_minicap_path).split()
            if "minicap.so" in minicap_files and ("minicap" in minicap_files or "minicap-nopie" in minicap_files):
                print(" >>> minicap was already installed.")
                return
        except:
            pass

        # install minicap
        local_minicap_path = "resources/minicap"
        try:
            adb.shell("mkdir %s 2>/dev/null" % self.remote_minicap_path)
        except Exception:
            pass
        abi = adb.get_property('ro.product.cpu.abi')
        sdk = adb.get_sdk_version()
        if sdk >= 16:
            minicap_bin = "minicap"
        else:
            minicap_bin = "minicap-nopie"
        self.device.push_file(local_file="%s/libs/%s/%s" % (local_minicap_path, abi, minicap_bin),
                            remote_dir=self.remote_minicap_path)
        self.device.push_file(local_file="%s/jni/libs/android-%s/%s/minicap.so" % (local_minicap_path, sdk, abi),
                            remote_dir=self.remote_minicap_path)
        print(" >>> minicap installed.")

    def tear_down(self):
        try:
            delete_minicap_cmd = "rm -r %s" % (self.remote_minicap_path)
            self.device.adb.shell(delete_minicap_cmd.split())
        except Exception:
            pass

    def connect(self):
        device = self.device

        display = device.get_display_info(refresh=True)
        if 'width' not in display or 'height' not in display or 'orientation' not in display:
            print(" <<< Cannot get the size of current device.")
            return
        w = display['width']
        h = display['height']
        o = display['orientation']

        size_opt = "%dx%d@%dx%d/%d" % (w, h, w, h, o)
        grant_minicap_perm_cmd = "adb -s %s shell chmod -R a+x %s" % \
                                 (device.adb.serial, self.remote_minicap_path)
        start_minicap_cmd = "adb -s %s shell LD_LIBRARY_PATH=%s %s/minicap -P %s" % \
                            (device.adb.serial, self.remote_minicap_path, self.remote_minicap_path, size_opt)
        print(" >>> starting minicap: " + start_minicap_cmd)

        p = subprocess.Popen(grant_minicap_perm_cmd.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = p.communicate()

        self.minicap_process = subprocess.Popen(start_minicap_cmd.split(),
                                                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # Wait 2 seconds for starting minicap
        time.sleep(1)
        print(" >>> minicap started.")

        try:
            # forward host port to remote port
            forward_cmd = "adb -s %s forward tcp:%d %s" % (device.adb.serial, self.port, MINICAP_REMOTE_ADDR)
            subprocess.check_call(forward_cmd.split())
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            import threading
            listen_thread = threading.Thread(target=self.listen_messages)
            listen_thread.start()
        except socket.error as e:
            self.connected = False
            print(" <<< ", e)
            pass

    def listen_messages(self):
        print(" >>> start listening minicap images ...")
        CHUNK_SIZE = 4096

        readBannerBytes = 0
        bannerLength = 2
        readFrameBytes = 0
        frameBodyLength = 0
        frameBody = bytearray()
        banner = {
            "version": 0,
            "length": 0,
            "pid": 0,
            "realWidth": 0,
            "realHeight": 0,
            "virtualWidth": 0,
            "virtualHeight": 0,
            "orientation": 0,
            "quirks": 0,
        }

        self.connected = True
        while self.connected:
            chunk = bytearray(self.sock.recv(CHUNK_SIZE))
            if not chunk:
                continue
            chunk_len = len(chunk)
            cursor = 0
            while cursor < chunk_len and self.connected:
                if readBannerBytes < bannerLength:
                    if readBannerBytes == 0:
                        banner['version'] = chunk[cursor]
                    elif readBannerBytes == 1:
                        banner['length'] = bannerLength = chunk[cursor]
                    elif 2 <= readBannerBytes <= 5:
                        banner['pid'] += (chunk[cursor] << ((readBannerBytes - 2) * 8))
                    elif 6 <= readBannerBytes <= 9:
                        banner['realWidth'] += (chunk[cursor] << ((readBannerBytes - 6) * 8))
                    elif 10 <= readBannerBytes <= 13:
                        banner['realHeight'] += (chunk[cursor] << ((readBannerBytes - 10) * 8))
                    elif 14 <= readBannerBytes <= 17:
                        banner['virtualWidth'] += (chunk[cursor] << ((readBannerBytes - 14) * 8))
                    elif 18 <= readBannerBytes <= 21:
                        banner['virtualHeight'] += (chunk[cursor] << ((readBannerBytes - 18) * 8))
                    elif readBannerBytes == 22:
                        banner['orientation'] += chunk[cursor] * 90
                    elif readBannerBytes == 23:
                        banner['quirks'] = chunk[cursor]

                    cursor += 1
                    readBannerBytes += 1
                    if readBannerBytes == bannerLength:
                        self.banner = banner
                        print("minicap initialized: %s" % banner)

                elif readFrameBytes < 4:
                    frameBodyLength += (chunk[cursor] << (readFrameBytes * 8))
                    cursor += 1
                    readFrameBytes += 1
                else:
                    if chunk_len - cursor >= frameBodyLength:
                        frameBody += chunk[cursor: cursor + frameBodyLength]
                        self.handle_image(frameBody)
                        cursor += frameBodyLength
                        frameBodyLength = readFrameBytes = 0
                        frameBody = bytearray()
                    else:
                        frameBody += chunk[cursor:]
                        frameBodyLength -= chunk_len - cursor
                        readFrameBytes += chunk_len - cursor
                        cursor = chunk_len
        print("<<< [CONNECTION] %s is disconnected" % self.__class__.__name__)

    def handle_image(self, frameBody):
        # Sanity check for JPG header, only here for debugging purposes.
        if frameBody[0] != 0xFF or frameBody[1] != 0xD8:
            self.logger.warning("Frame body does not start with JPG header")
        self.last_screen = frameBody
        self.last_screen_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        # print(" >>> Received an image at %s" % self.last_screen_time)

    def disconnect(self):
        """
        disconnect telnet
        """
        self.connected = False
        if self.sock is not None:
            try:
                self.sock.close()
            except Exception as e:
                print(e)
        if self.minicap_process is not None:
            try:
                self.minicap_process.terminate()
            except Exception as e:
                print(e)
        try:
            forward_remove_cmd = "adb -s %s forward --remove tcp:%d" % (self.device.adb.serial, self.port)
            p = subprocess.Popen(forward_remove_cmd.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = p.communicate()
        except Exception as e:
            print(e)

    def update_device(self, device):
        self.device = device

if __name__ == "__main__":
    adb = ADB("emulator-5556")
    device = Device(adb)

    minicap = Minicap(device)
    minicap.set_up()
    minicap.connect()

    time.sleep(20)
    minicap.disconnect()
    minicap.tear_down()
