import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from sklearn.cluster import KMeans
from itertools import groupby
import math
import matplotlib.pyplot as plt
from PIL import Image
import glob
import tqdm
import json





np.random.seed(42)

class VideoScene:
    def __init__(self, video, stable_duration=1, stable_threshold=0.99, num_unstable=3, 
                            GESTURE_FOLDER=None, OUTPUT_STABLE_DIR=None, OUTPUT_UNSTABLE_DIR=None):
        self.video = video
        self.app = self.video.split('/')[-4]
        self.trace_no = self.video.split('/')[-3]
        self.gifid = self.video.split('/')[-1].replace('.gif','')
        self.GESTURE_FOLDER = GESTURE_FOLDER
        self.gesture = self.get_gesture()

        self.stable_duration = stable_duration
        self.stable_threshold = stable_threshold
        self.k_means = num_unstable

        self.OUTPUT_STABLE_DIR = OUTPUT_STABLE_DIR
        self.OUTPUT_UNSTABLE_DIR = OUTPUT_UNSTABLE_DIR


        if len(self.gesture) > 1 or len(self.gesture) == 0:
            self.frames, self.y_frames = [], []
            self.sim_sequence = []
            self.shots = None
        else:
            self.frames, self.y_frames = self.get_frames_from_video()

            # frame difference
            self.sim_sequence = self.get_sim_seq()

            # group the frames
            self.shots = self.detect_shots()
    
    def get_gesture(self):
        gesture_file = os.path.join(self.GESTURE_FOLDER, f'{self.app}/{self.trace_no}/gestures.json')
        if not os.path.exists(gesture_file):
            return []
        with open(gesture_file, 'r') as f:
            data = json.loads(f.read())
        if self.gifid in data.keys():
            gesture = data[self.gifid]
        else:
            gesture = []
        return gesture

    def get_frames_from_video(self):
        frames = []
        y_frames = []
        vidcap = cv2.VideoCapture(self.video)
        success, frame = vidcap.read()
        frames.append(frame)
        y_frame = extract_Y(frame)
        y_frames.append(y_frame[15:])
        while success: 
            success, frame = vidcap.read()  
            if not success:
                break
            frames.append(frame)
            y_frame = extract_Y(frame)
            y_frames.append(y_frame[15:])    
        vidcap.release()

        return frames, y_frames

    def get_sim_seq(self):
        sim_list = [1]
        for i in range(0, len(self.y_frames)-1):
            sim = ssim(self.y_frames[i], self.y_frames[i+1])
            sim_list.append(sim)
             
        return sim_list
    
    def visualize_sim_seq(self):
        plt.plot(np.arange(len(self.sim_sequence)), np.array(self.sim_sequence))
        plt.show()

    def visualize_frames(self, i):
        plt.subplot(1, 2, 1)
        plt.imshow(self.frames[i])
        plt.axis('off')
        plt.subplot(1, 2, 2)
        plt.imshow(self.frames[i+1])
        plt.axis('off')
        # plt.subplot(1, 3, 3)
        # plt.imshow(diff)
        # plt.axis('off')
        plt.show()
    

    def is_stable(self, start, end):
        if start < 0: start = 0
        if end > len(self.sim_sequence): end = len(self.sim_sequence)
        return all(x > self.stable_threshold for x in self.sim_sequence[start:end])

    def detect_shots(self):
        """
        Detect the shots into stable or transition
        
        Returns
        -------
        shots  : [start_idx, end_idx, (-1: stable, 1: transition)]
        """
        stable_list = [self.is_stable(idx-self.stable_duration, idx+self.stable_duration) for idx in range(len(self.sim_sequence))]
        zipped = zip(stable_list, range(len(stable_list)))

        shot_list = []
        for k, g in groupby(zipped, lambda x: x[0]):
            group_ = list(g).copy()
            # Stable
            if k:
                shot_list.append([group_[0][1], group_[-1][1], -1])
            # UnStable
            else:
                shot_list.append([group_[0][1], group_[-1][1], 1])

        assert shot_list[0][0] == 0, "Shots are not beginning from 0"
        assert shot_list[-1][1] == len(stable_list)-1, "Shots are not ending"

        return np.array(shot_list)
    
    def get_frames(self):
        return self.frames

    def get_shots(self):
        return self.shots

    def write_dataset(self):
        if self.shots is None:
            return None
        for shot in self.shots:
            if shot[2] == -1:
                selected_idx = math.floor((shot[0]+shot[1]) / 2)
                cv2.imwrite(f'{self.OUTPUT_STABLE_DIR}/{self.app}-{self.gifid}-{selected_idx}.jpg', self.frames[selected_idx])
            else:
                unstable_frames = [self.y_frames[i].flatten() for i in range(shot[0], shot[1]+1)]
                unstable_frames = np.array(unstable_frames)
                kmeans = KMeans(n_clusters=min(self.k_means, unstable_frames.shape[0]),
                                        init='random',random_state = 42)
                kmeans.fit(unstable_frames)
                Z = kmeans.predict(unstable_frames)
                selected_idx = [shot[0]+np.where(Z==i)[0] for i in range(0,min(self.k_means, unstable_frames.shape[0])) 
                                                            if len(np.where(Z==i)[0])>0]
                selected_idx = [interval[0] for interval in selected_idx if len(self.frames)-1 not in interval]
                for selected in selected_idx:
                    cv2.imwrite(f'{self.OUTPUT_UNSTABLE_DIR}/{self.app}-{self.gifid}-{selected}.jpg', self.frames[selected])


def extract_Y(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, _, _ = cv2.split(img_yuv)
    return y


if __name__ == "__main__":
    '''
        Visualize single video
    '''
    video = '/Rico/animations/com.famousbluemedia.yokee/trace_0/gifs/922.gif'
    vs = VideoScene(video)
    shots = vs.get_shots()
    vs.visualize_sim_seq()