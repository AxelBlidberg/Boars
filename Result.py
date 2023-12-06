import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def PlotFlowerAmount(ax1, ax2, fData):
    trends = [[], [], [], [], []]
    labels = ['Lavender', 'Bee balm', 'Sunflower', 'Coneflower', 'Blueberry']
    colors = ['purple', 'red', 'orange', 'pink', 'blue']
    amount = []
    
    for i, season in enumerate(fData):
        for j, quarter in enumerate(season):
            values = []
            for k, label in enumerate(labels):
                values.append(quarter[label])
                trends[k].append(quarter[label])
            amount.append(np.sum(values))
    x = np.linspace(0, len(fData)-1, num=len(trends[0]))
    ax1.plot(x, amount)
    for i in range(len(trends)):
        ax2.plot(x, trends[i])

    ax1.set_title('Total flower amount')
    ax1.set_xlabel('Seasons')
    ax1.set_ylabel('n Flowers')
    ax2.set_title('Flower distribution')
    ax2.set_xlabel('Seasons')
    ax2.set_ylabel('n Flowers')
    ax2.legend(labels=labels, loc='center left', bbox_to_anchor=(1, 0.75))
    return x, amount

def PlotBeePopulation(ax1, bData, x):
    labels = ['Small Bee', 'Intermediate Bee', 'Bee population']
    colors = ['blue', 'red', 'gray']
    trends = [[], []]
    amount = []
    print('Lengths: ', len(bData))
    for i in bData:
        print(len(i))

    for i, season in enumerate(bData):
        for j, quarter in enumerate(season):
            values = []
            for k in range(len(labels)-1):
                values.append(quarter[k])
                trends[k].append(quarter[k])
            amount.append(np.sum(values))

    ax1.plot(x, amount, color=colors[2])
    
    for i in range(len(trends)):
        ax1.plot(x, trends[i], color=colors[i])

    ax1.set_title('Bee population')
    ax1.set_xlabel('Seasons')
    ax1.set_ylabel('n Bees')
    ax1.legend(labels=labels, loc='center left', bbox_to_anchor=(1, 0.9))
    return amount

def PlotFlowerBeeDensity(ax, fData, bData, x):
    trend = [fData[i] / bData[i] for i in range(len(fData))]
    ax.plot(x, trend)
    ax.set_title('Flowers / Bee')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('Flowers / Bee')

def PlotAvgLifespan(ax, lData):
    ax.set_title('Average Lifespan (Bees)')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('Time')

def MergePlots(flowerData, beeData, lifespanData):
    #SaveFunction(flowerData, beeData)
    fig, axs = plt.subplots(3, 3, gridspec_kw={'hspace': 0.5, 'wspace': 0.75})
    axs[0, 0].get_shared_x_axes().join(axs[0, 0], axs[1, 0])
    axs[0, 1].get_shared_x_axes().join(axs[0, 1], axs[1, 1])
    x, fPop = PlotFlowerAmount(axs[0, 0], axs[1,0], flowerData)  # Pass individual subplot
    bPop = PlotBeePopulation(axs[0, 1], beeData, x)  # Pass individual subplot
    PlotAvgLifespan(axs[1, 1], lifespanData)    # Pass individual subplot
    PlotFlowerBeeDensity(axs[2, 0], fPop, bPop, x)  # Pass individual subplot
    plt.show()

fData = [[{'Lavender': 17, 'Bee balm': 17, 'Sunflower': 24, 'Coneflower': 51, 'Blueberry': 41},{'Lavender': 17, 'Bee balm': 17, 'Sunflower': 24, 'Coneflower': 51, 'Blueberry': 41},{'Lavender': 17, 'Bee balm': 17, 'Sunflower': 0, 'Coneflower': 0, 'Blueberry': 0},{'Lavender': 126, 'Bee balm': 70, 'Sunflower': 40, 'Coneflower': 172, 'Blueberry': 223}],
        [{'Lavender': 126, 'Bee balm': 70, 'Sunflower': 40, 'Coneflower': 172, 'Blueberry': 223},{'Lavender': 126, 'Bee balm': 70, 'Sunflower': 40, 'Coneflower': 172, 'Blueberry': 223},{'Lavender': 126, 'Bee balm': 70, 'Sunflower': 0, 'Coneflower': 0, 'Blueberry': 0},{'Lavender': 255, 'Bee balm': 113, 'Sunflower': 19, 'Coneflower': 153, 'Blueberry': 175}],
        [{'Lavender': 255, 'Bee balm': 113, 'Sunflower': 19, 'Coneflower': 153, 'Blueberry': 175},{'Lavender': 255, 'Bee balm': 113, 'Sunflower': 19, 'Coneflower': 153, 'Blueberry': 175},{'Lavender': 255, 'Bee balm': 113, 'Sunflower': 0, 'Coneflower': 0, 'Blueberry': 0},{'Lavender': 153, 'Bee balm': 78, 'Sunflower': 5, 'Coneflower': 79, 'Blueberry': 99}],
        [{'Lavender': 153, 'Bee balm': 78, 'Sunflower': 5, 'Coneflower': 79, 'Blueberry': 99},{'Lavender': 153, 'Bee balm': 78, 'Sunflower': 5, 'Coneflower': 79, 'Blueberry': 99},{'Lavender': 153, 'Bee balm': 78, 'Sunflower': 0, 'Coneflower': 0, 'Blueberry': 0},{'Lavender': 308, 'Bee balm': 80, 'Sunflower': 0, 'Coneflower': 53, 'Blueberry': 63}]]
bData = [[{'Small Bee': 4, 'Intermediate Bee': 9, 'Large Bee': 7},{'Small Bee': 4, 'Intermediate Bee': 9, 'Large Bee': 7},{'Small Bee': 4, 'Intermediate Bee': 9, 'Large Bee': 7},{'Small Bee': 3, 'Intermediate Bee': 7, 'Large Bee': 6}],[
            {'Small Bee': 0, 'Intermediate Bee': 1, 'Large Bee': 4},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 4},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 4},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 4}],
            [{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 4},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 0},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 0},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 2}],
            [{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 2},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 2},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 2},{'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 6}]]

#MergePlots(fData, bData, [])