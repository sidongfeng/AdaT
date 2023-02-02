# Data Preparation
<p align="center">
<img src="../../figures/dataset.png" width="80%"/> 
</p>
<p align="center">Figure: Pipeline for automated data collection.<p align="center">

The goal of this phase is to automatically collect partially rendered GUIs and fully rendered GUIs by leveraging GUI transiting screencasts, as shown in Figure.

## Overview

- **GUI Transiting Screencasts.**
We leverage the open-sourced Rico dataset, which contains 44,418 transiting screencasts from more than 9.7k different Android applications in 27 different app categories.

- **Transiting Frame Identification.**
To identify the frame state in the transiting screencast, we adopt an image processing technique to build a perceptual similarity score for consecutive frame comparison based on Y-Difference. 

- **GUI State Sampling.**
To prevent bias on redundant data, we propose to sample the GUI frames from GUI groups.
As the GUI frames in the fully rendered group are similar or identical, we randomly select one frame.
To sample frames from partially rendered groups, we adopt a paradigm using uniform sampling.





## Dataset Construction

1. Download Rico dataset.
* `Rico`: https://interactionmining.org/rico

> **Note:** We discard the transiting periods of scroll action in our dataset as the GUI state can be ambiguous on the development mechanism. Thus, we obtain 36,038 transiting screencasts.

2. Run the dataset construction.
```
ANIMATION_FOLDER = '/Rico/animations' # Rico ANIMATIONS
GESTURE_FOLDER = '/Rico/filtered_traces' # Rico INTERACTION TRACES
NUM_UNSTABLE = 3 # sample number of frames from partially rendered group
OUTPUT_DIR = './dataset'

python dataset.py
```

3. The dataset would be well splitted in `OUTPUT_DIR` with train, val, and test folders. 

> **Note:** We split the dataset on apps to prevent data leakage.



