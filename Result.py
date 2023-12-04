import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def PlotFlowerAmount(ax, fData):
    labels = ['Lavender', 'Bee balm', 'Sunflower', 'Coneflower', 'Blueberry']
    colors = ['purple', 'red', 'orange', 'pink', 'blue']
    oldSum = -1

    for i, line in enumerate(fData):
        values = []
        print(line)
        for j,l in enumerate(labels):
            values.append(line[l])
            ax.plot([i, i+1], [line[l], line[l]], color=colors[j])

        ax.plot([i, i+1], [np.sum(values), np.sum(values)], color='gray', linewidth=2, marker='o')
        if oldSum != -1:
            ax.plot([i, i], [oldSum, np.sum(values)], '--', linewidth=1, color='gray')
        oldSum = np.sum(values)
    

    labels.append('Total amount')
    ax.set_title('Flower population and distribution')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('n Flowers')
    ax.legend(labels=labels, loc='center left', bbox_to_anchor=(1, 0.75))
    #help(ax.legend(labels=labels))

def PlotBeePopulation(ax, bData):
    labels = ['Small Bee', 'Intermediate Bee']
    colors = ['blue', 'red']

    for i, season in enumerate(bData):
        for j, quarter in enumerate(season):
            pass

    ax.set_title('Bee population')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('n Bees')

def PlotFlowerBeeDensity(ax, fData, bData):
    ax.set_title('Flowers / Bee')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('Flowers / Bee')

def PlotAvgLifespan(ax, lData):
    ax.set_title('Average Lifespan (Bees)')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('Time')

def MergePlots(flowerData, beeData, lifespanData):
    print('Enter')
    fig, axs = plt.subplots(2, 2, gridspec_kw={'hspace': 0.5, 'wspace': 0.5})
    PlotFlowerAmount(axs[0, 0], flowerData)  # Pass individual subplot
    PlotBeePopulation(axs[0, 1], beeData)  # Pass individual subplot
    PlotAvgLifespan(axs[1, 1], lifespanData)    # Pass individual subplot
    PlotFlowerBeeDensity(axs[1, 0], flowerData, beeData)  # Pass individual subplot
    plt.show()
