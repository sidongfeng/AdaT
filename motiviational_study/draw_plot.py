import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def draw_automated_testing_tools_barplot():     
    x = ['Ape', 'Monkey', 'Droidbot']
    y1 = np.array([192/1646*100, 678/2830*100, 137/875*100])
    y2 = np.array([70/1646*100, 175/2830*100, 55/875*100])
    y3 = np.array([41/1646*100, 97/2830*100, 25/875*100])
    y4 = np.array([1343/1646*100, 1880/2830*100, 658/875*100])
    fig, ax = plt.subplots()
    line1 =ax.barh(x, y1, height=0.6, color=np.array([57/255, 81/255, 162/255, 1]), edgecolor='black', label="Transiting state")
    line2 =ax.barh(x, y2, height=0.6, color=np.array([114/255, 170/255, 207/255, 1]), left=y1, edgecolor='black', label="Explicit loading")
    line3 =ax.barh(x, y3, height=0.6, color=np.array([253/255, 185/255, 107/255, 1]), left=y1+y2, edgecolor='black', label="Implicit loading")
    line4 =ax.barh(x, y4, height=0.6, color=np.array([236/255, 93/255, 59/255, 1]), left=y1+y2+y3, edgecolor='black', label="Fully rendered")

    plt.xlabel('State Distribution', fontsize=18)
    plt.ylabel('Automated Testing Tools', fontsize=18)
    plt.yticks(fontsize=16)
    ax.legend(handles=[line1, line2, line3, line4],
                loc='upper center', bbox_to_anchor=(0.5, 1.15),
                ncol=4, fancybox=True, shadow=True, fontsize=16, frameon=True, handletextpad=0.3, columnspacing=1)   

    plt.show()

def draw_efficiency_of_throttle_barplot():
    x = ['200ms', '400ms', '600ms', '800ms', '1000ms']
    y1 = np.array([192, 102, 60, 31, 26])
    y2 = np.array([70, 67, 54, 39, 29])
    y3 = np.array([41, 38, 25, 16, 14])
    y4 = np.array([1343, 1092, 884, 821, 701])
    y5 = np.array([25.8, 25.3, 26.1, 24.5, 21])
    fig, ax = plt.subplots()
    line1 =ax.bar(x, y1, width=0.6, color=np.array([57/255, 81/255, 162/255, 1]), edgecolor='black', label="Transiting state")
    line2 =ax.bar(x, y2, width=0.6, color=np.array([114/255, 170/255, 207/255, 1]), bottom=y1, edgecolor='black', label="Explicit loading")
    line3 =ax.bar(x, y3, width=0.6, color=np.array([253/255, 185/255, 107/255, 1]), bottom=y1+y2, edgecolor='black', label="Implicit loading")
    line4 =ax.bar(x, y4, width=0.6, color=np.array([236/255, 93/255, 59/255, 1]), bottom=y1+y2+y3, edgecolor='black', label="Fully rendered")
    plt.ylabel('Number of GUI', fontsize=18)
    plt.xticks(fontsize=15)
    plt.xlabel('Throttle for Droidbot', fontsize=18)
    
    ax2 = ax.twinx()
    line5, = ax2.plot(x, y5, color=np.array([6/255, 1/255, 250/255, 1]), marker="o", linewidth=2, label="Coverage")
    plt.ylabel('Activity Coverage (%)', fontsize=16)

    # ax.legend(handles=[line4, line3, line2, line1, line5],
    #             fancybox=True, shadow=True, fontsize=16, frameon=True)  
    ax.legend(handles=[line4, line3, line2, line1, line5],
                fancybox=True, shadow=True, fontsize=16, frameon=True,
                loc='center left', bbox_to_anchor=(1.10, 0.5))
    plt.show()


if __name__ == '__main__': 
    draw_automated_testing_tools_barplot()
    # draw_efficiency_of_throttle_barplot()
    