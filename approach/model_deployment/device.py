import os
import random


class Device(object):
    """
    this class describes a connected device
    """

    def __init__(self, adb, output_dir=None):
        self.output_dir = output_dir
        self.adb = adb

        self.height = None
        self.width = None
        self.display_info = None
    
    def pull_file(self, remote_file, local_file):
        self.adb.run_cmd(["pull", remote_file, local_file])

    def take_screenshot(self, img_save_path):
        if self.output_dir is None:
            return None
        
        remote_image_path = f"/sdcard/{img_save_path}"
        self.adb.shell("screencap -p %s" % remote_image_path)

        local_image_path = os.path.join(self.output_dir, img_save_path)
        self.pull_file(remote_image_path, local_image_path)
        self.adb.shell("rm %s" % remote_image_path)
        return local_image_path
    
    def get_height(self):
        if self.height is None:
            size = self.adb.shell('wm size').split('Physical size:')[-1]
            self.height = int(size.split('x')[1])
        return self.height

    def get_width(self):
        if self.width is None:
            size = self.adb.shell('wm size').split('Physical size:')[-1]
            self.width = int(size.split('x')[0])
        return self.width

    def get_random_port(self):
        return random.randint(1000,9999)

    def push_file(self, local_file, remote_dir="/sdcard/"):
        """
        push file/directory to target_dir
        :param local_file: path to file/directory in host machine
        :param remote_dir: path to target directory in device
        :return:
        """
        if not os.path.exists(local_file):
            print(" <<< push_file file does not exist: %s" % local_file)
        self.adb.run_cmd(["push", local_file, remote_dir])
    
    def get_display_info(self, refresh=True):
        """
        get device display information, including width, height, and density
        :param refresh: if set to True, refresh the display info instead of using the old values
        :return: dict, display_info
        """
        if self.display_info is None or refresh:
            self.display_info = {'width': self.get_width(),
                                    'height': self.get_height(),
                                    'orientation': 0}
        return self.display_info