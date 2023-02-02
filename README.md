# Efficiency Matters: Speeding Up Automated Testing with GUI Rendering Inference

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
- [Motiviational Study](#motiviational-study)
    - [Categorizing GUI rendering state](#categorizing-gui-rendering-state)
    - [Are partially rendered states common in testing tools?](#are-partially-rendered-states-common-in-testing-tools)
    - [How to address partially rendered states?](#how-to-address-partially-rendered-states)
    - [Why makes throttle adaptive?](#why-makes-throttle-adaptive)
- [Approach](#approach)
    - [Data Preparation](#data-preparation)
    - [GUI Rendering State Classification](#gui-rendering-state-classification)
    - [Model Deployment](#model-deployment)
- [Evaluation](#evaluation)
    - [RQ1: Performance of Model](#rq1-performance-of-model)
    - [RQ2: Performance of AdaT](#rq2-performance-of-AdaT)
    - [RQ3: Usefulness of AdaT](#rq3-usefulness-of-AdaT)


## Getting Started
<p align="center">
<img src="figures/timeline.png" width="90%"/> 
</p>
<p align="center">Figure: Automated GUI testing with different throttle.<p align="center">

Due to the importance of Android app quality assurance, many automated testing tools have been developed.
Although the test algorithms have been improved, they still face the issue of striking a balance between effectiveness and efficiency.
On the one hand, setting long waiting time (e.g., Figure 800ms) to execute events on fully rendered GUIs slows down the testing process.
On the other hand, setting short waiting time (e.g., Figure 200ms 400ms) will cause the events execute on partially rendered GUIs, which negatively affects the testing effectiveness.
An optimal waiting time should striking a balance between effectiveness and efficiency.

While the app under testing is mostly idle, the tool has to wait until the GUI finishes rendering before moving to the next event.
To that end, we propose AdaT, a lightweight image-based approach to dynamically adjust the inter-event time based on GUI rendering inference.
Given the real-time streaming on the GUI, AdaT adopts a deep learning model to infer the rendering state, and synchronizes with the testing tool to schedule the next event when the GUI is fully rendered.

## Motiviational Study
To better understand the issues of automated testing tools with throttling, we carried out a pilot study to examine the prevalence of these issues, so as to facilitate the development of our tool to enhance the existing Android testing tools.

> For more details and experimental setup, please check the instructions in [README.md](./motiviational_study)

### Categorizing GUI rendering state
<p align="center">
<img src="figures/partially_example.png" width="60%"/> 
</p>


* **Fully Rendered State.** A fully rendered state represents a complete transition to the GUI with all resources loaded.

* **Transiting State.** One state is transiting to the next state.
As the transition between states takes longer than the throttle, two GUIs are overlapped with each other.

* **Explicit Loading State.** Depicts a loading bar in the GUI, such as spinning wheel, linear progressing bar, etc.
It explicitly indicates the process or rendering is in progress.

* **Implicit Loading State.** Some resources are not showing due to network latency or resource defects.

By conducting a pilot study on Droidbot, we categorize four types of GUI rendering states that lie into fully rendered states, and partially rendered states (e.g., transiting state, explicit loading state, and implicit loading state)

### Are partially rendered states common in testing tools?
<p align="center">
<img src="figures/stacked_percent.png" width="70%"/> 
</p>
<p align="center">Figure: Distribution of rendering states captured by Droidbot, Monkey, and Ape.<p align="center">

By analyzing three commonly-used testing tools, we find that they all encounter the issue with partially rendered states, which may negatively influence the effectiveness when testing.


### How to address partially rendered states?
<p align="center">
<img src="figures/throttle_affect.png" width="70%"/> 
</p>
<p align="center">Figure: Number of GUIs and activity coverage in different throttle settings of Droidbot.<p align="center">

By analyzing five different throttle intervals, we find that extending throttle can help address the issue with partially rendered states.
However, an excessive long throttle can reduce the efficiency of automated exploration.

### Why makes throttle adaptive?
These findings confirm the importance of throttle setting to automated testing, and motivate us to design an approach for balancing effectiveness and efficiency. Taken in this sense, it is worthwhile developing a new effective and efficient method to dynamically adjust the throttle during testing.

## Approach
<p align="center">
<img src="figures/overview.png" width="60%"/> 
</p>
<p align="center">Figure: The overview of AdaT.<p align="center">

This paper proposes a simple but effective approach AdaT to adaptively adjust the throttle base on GUI screenshots.
Given that automated testing tools test on the device, we synchronously stream the GUI screenshot capturing, and detect its current rendering state.
Based on the GUI rendering inference, we schedule the testing events, which will be sent if the GUI is fully rendered, otherwise, wait explicitly for rendering.

> For more approach details and experimental settings, please check the instructions in [README.md](./approach)

### Data Preparation
<p align="center">
<img src="figures/dataset.png" width="80%"/> 
</p>
<p align="center">Figure: Pipeline for automated data collection.<p align="center">

The foundation of understanding GUI rendering state and training deep learning model is big data, whereas manual labeling is prohibitively expensive.
We leverage image processing techniques to extract frames from GUI transiting screencasts to automated construct a large-scale binary GUI dataset, including 66,233 fully rendered and 45,623 partially rendered GUIs. 

### GUI Rendering State Classification
We adopt an implementation of MobileNetV2, which distills the best practices in convolutional network design into a simple architecture to identify whether the GUI is fully rendered which allows testing tools to execute the next event; or whether the GUI is partially rendered which waits until the rendering is complete.

### Model Deployment
<p align="center">
<img src="figures/implementation.png" width="60%"/> 
</p>
<p align="center">Figure: Overview of model deployment.</p>
To make the model efficiently provide feedback of GUI rendering state to the automated testing tool, synchronization of the GUI and the testing tool is needed.
Therefore, we develop a socket-based smartphone test farm using OpenSTF to stream the real time GUI screenshot.

Once the screenshot buffer is received, we decode it into a PyTorch tensor.
This tensor is then fed into our trained GUI state classification model to infer the rendering state of current GUI.
If it is fully rendered, we continue to test on the new event, otherwise, we explicitly wait for the next screenshot buffer.

## Evaluation
The main quality of our study is the extent to whether our AdaT can effectively and efficiently accelerate the automated testing process.
To achieve our study goals, we formulate the following three research questions:

- **RQ1:** How accurate is our model in classifying GUI rendering state?
- **RQ2:** How effective and efficient is our approach in triggering bugs?
- **RQ3:** How useful is our approach when integrated in real-world automated testing tools?

For RQ1, we first present some general performance of our model for GUI rendering inference and the comparison with state-of-the-art baselines.
For RQ2, we carry out experiments to check if our tool can speed up the automated GUI testing, without sacrificing the effectiveness of bug triggering.
For RQ3, we integrate AdaT with DroidBot as an enhanced automated testing tool to measure the ability of our approach in real-world testing environments.

> For more details and experimental setup, please check the instructions in [README.md](./evaluation)

### RQ1: Performance of Model
<p align="center">
<img src="figures/rq1.png" width="40%"/> 
</p>

The performance of our model is much better than that of other baselines, i.e., improves 13.6%, 18%, 16% in recall, precision, and F1-score compared with the best baseline (CNN). In addition, our model takes on average 43.02ms per GUI inference, representing the ability of our model to accurately and efficiently discriminate the GUI rendering state.

### RQ2: Performance of AdaT
<p align="center">
<img src="figures/rq2.png" width="95%"/> 
</p>


AdaT takes an average of 15.93 seconds to reproduce all the bugs. The throttling methods cannot trigger all the bugs, and may trigger the bug that will not be encountered by real-world users. Themis can trigger all of the bugs, but it takes much longer time, on average 31.31 seconds, which is 2x slower than our approach. In addition, leveraging deep learning model and real-time GUI rendering monitor speeds up the testing process than that of the abalation baselines.
In addition, our approach of using single GUI screenshot and real-time GUI rendering monitor speeds up the testing process.
As a result, AdaT does not affect the capability to trigger the bugs, especially those caused by partially rendered GUIs; on the other hand, AdaT can speed up the automated testing, saving much of the time budget in hundreds or thousands of steps in long-term testing.

### RQ3: Usefulness of AdaT
<p align="center">
<img src="figures/rebuttal_2.png" width="50%"/> 
</p>

Droidbot+AdaT achieves a median activity coverage of 43.14% across 32 Android apps, which is 6.95% higher even compared with the best baseline (e.g., 36.19% in Throttle 200ms). In addition, Droidbot+AdaT explores 3,207 GUI states, and 88.81% are fully rendered, indicating the effectiveness and efficiency of our approach in covering most of the activities, bugs, and fully rendered GUIs in real-world testing environments.

## Citations
Please consider citing this paper if you use the code:
```
@article{feng2023efficiency,
  title={Efficiency Matters: Speeding Up Automated Testing with GUI Rendering Inference},
  author={Feng, Sidong and Xie, Mulong and Chen, Chunyang},
  booktitle={2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)},
  year={2023},
  organization={IEEE}
}
```