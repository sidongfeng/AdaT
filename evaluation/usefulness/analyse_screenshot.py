import os
import glob
import json
import shutil

class Droidbot(object):
    def __init__(self, droidbot_output):
        self.droidbot_output = droidbot_output
    
    def get_screenshots(self):
        if os.path.isdir(os.path.join(self.droidbot_output, 'clean_states')):
            return glob.glob(os.path.join(self.droidbot_output, 'clean_states', '*.jpg'))
        else:
            return glob.glob(os.path.join(self.droidbot_output, 'states', '*.jpg'))


def get_annotation(annotation_dir):
    return len(glob.glob(os.path.join(annotation_dir, '*.json')))


if __name__ == '__main__': 
    droidbot_dir = 'usefulness_output/origin_10min_600'
    annotation_dir = 'usefulness_output/origin_10min_600_annotation'
    
    screenshots = []
    for droidbot_output in glob.glob(os.path.join(droidbot_dir, '*/')):
        app_name = droidbot_output.split('/')[-2]

        droidbot = Droidbot(droidbot_output)
        screenshot = droidbot.get_screenshots()
        screenshots.extend(screenshot)

    annotation_no = get_annotation(annotation_dir)
    screenshot_no = len(screenshots)
    print(' >>> Number of Annotation: {}'.format(annotation_no))
    print(' >>> Number of Screenshot: {}'.format(screenshot_no))
    print(' >>> Ratio: {}'.format(annotation_no/screenshot_no))