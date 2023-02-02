import os
import glob
import json
import shutil

class Droidbot(object):
    def __init__(self, droidbot_output, fastbot_output):
        self.droidbot_output = droidbot_output
        self.fastbot_output = fastbot_output

        self.test_activities = self.get_test_activities()
        self.total_activities = self.get_total_activities()
    
    def get_test_activities(self):
        activities = []
        for json_file in glob.glob(os.path.join(self.droidbot_output, 'states/*.json')):
            with open(json_file, 'r') as reader:
                data = json.loads(reader.read())
            activity_stack = data['activity_stack']
            activities.extend(activity_stack)
        activities = list(set(activities))
        activities = [act.replace('/','') for act in activities]
        return activities

    def get_total_activities(self):
        log_file = glob.glob(os.path.join(self.fastbot_output, '*/max.activity.statistics.log'))[0]
        with open(log_file, 'r') as reader:
            # lines = [line.for line in reader.readlines()]
            data = json.loads(reader.read())
        return data['TotalActivity']

    def count_coverage(self):
        # counted_activities = []
        # for activity in self.test_activities:
        #     if activity in self.total_activities:
        #         counted_activities.append(activity)
        #     else:
        #         self.total_activities.append(activity)
        #         counted_activities.append(activity)
        counted_activities = [activity for activity in self.test_activities 
                                            if activity in self.total_activities]
        return len(counted_activities) / len(self.total_activities)
    
    def get_screenshots(self):
        if os.path.isdir(os.path.join(self.droidbot_output, 'clean_states')):
            return glob.glob(os.path.join(self.droidbot_output, 'clean_states', '*.jpg'))
        else:
            return glob.glob(os.path.join(self.droidbot_output, 'states', '*.jpg'))


if __name__ == '__main__': 
    droidbot_dir = 'usefulness_output/origin_10min_1000'
    fastbot_dir = 'usefulness_output/activities'
    
    coverages = []
    screenshots = []
    for droidbot_output in glob.glob(os.path.join(droidbot_dir, '*/')):
        app_name = droidbot_output.split('/')[-2]
        fastbot_output = os.path.join(fastbot_dir, app_name)

        droidbot = Droidbot(droidbot_output, fastbot_output)
        screenshot = droidbot.get_screenshots()
        screenshots.extend(screenshot)
        coverage = droidbot.count_coverage()
        coverages.append(coverage)

        for s in screenshot:
            output_dir = 'usefulness_output/images'
            from_ = s
            to_ = os.path.join(output_dir, '{}_{}'.format(app_name, s.split('/')[-1])) 
            # shutil.copyfile(from_, to_)

    print(' >>> Number of screenshots: {}'.format(sum(screenshots)))
    print(' >>> Activity Mean Coverage: {}'.format(sum(coverages)/len(coverages)))