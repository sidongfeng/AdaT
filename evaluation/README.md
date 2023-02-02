# Evaluation

The main quality of our study is the extent to whether our Throttledroid can effectively and efficiently accelerate the automated testing process.
To achieve our study goals, we formulate the following three research questions:

- **RQ1:** How accurate is our model in classifying GUI rendering state?
- **RQ2:** How effective and efficient is our approach in finding bugs?
- **RQ3:** How useful is our approach when integrated in real-world automated testing tools?

## RQ1: Performance of Model
<p align="center">
<img src="../figures/rq1.png" width="40%"/> 
</p>

1. We set up 10 baseline methods, including machine learning-based and deep learning-based, that are widely used in image classification tasks as the baselines to compare with our model. 
    - To reproduce the experiments, please follow the instructions in [`model_performance`](./model_performance).

> The performance of our model is much better than that of other baselines, i.e., improves 13.6%, 18%, 16% in recall, precision, and F1-score compared with the best baseline (CNN). In addition, our model takes on average 43.02ms per GUI inference, representing the ability of our model to accurately and efficiently discriminate the GUI rendering state.

## RQ2: Performance of AdaT
<p align="center">
<img src="../figures/rq2.png" width="95%"/> 
</p>

1. We set up 6 throttling methods and 2 ablation study as our baselines to compare with our approach.
    - To reproduce the experiments, please follow the instructions in [`adat_performance`](./adat_performance).

> AdaT takes an average of 15.93 seconds to reproduce all the bugs. The throttling methods cannot trigger all the bugs, and may trigger the bug that will not be encountered by real-world users. Themis can trigger all of the bugs, but it takes much longer time, on average 31.31 seconds, which is 2x slower than our approach. In addition, our approach of using single GUI screenshot and real-time GUI rendering monitor speeds up the testing process.
As a result, AdaT does not affect the capability to trigger the bugs, especially those caused by partially rendered GUIs; on the other hand, AdaT can speed up the automated testing, saving much of the time budget in hundreds or thousands of steps in long-term testing.

## RQ3: Usefulness of AdaT
<p align="center">
<img src="../figures/rq3.png" width="50%"/> 
</p>

1. To demonstrate how our AdaT can affect real-world testing environments, we integrated our approach into the mature automated testing tool Droidbot, namely Droidbot+AdaT. In detail, Droidbot+AdaT is adaptive to GUI rendering, moving to the next event as soon as GUI rendering is complete.
    - To reproduce the experiments, please follow the instructions in [`usefulness`](./usefulness).

> Droidbot+AdaT achieves a median activity coverage of 43.14% across 32 Android apps, which is 6.95% higher even compared with the best baseline (e.g., 36.19% in Throttle 200ms). In addition, Droidbot+AdaT explores 3,207 GUI states, and 88.81% are fully rendered, indicating the effectiveness and efficiency of our approach in covering most of the activities and fully rendered GUIs in real-world testing environments.