import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def PlotFlowerAmount(ax, data):
    labels = ['Lavender', 'Bee balm', 'Sunflower', 'Coneflower', 'Blueberry']
    colors = ['purple', 'red', 'orange', 'pink', 'blue']
    encoding = [1, 2, 3, 4, 5]
    oldSum = -1

    for i, line in enumerate(data):
        values = []
        print(line)
        for j,l in enumerate(labels):
            values.append(line[l])
            ax.plot([i, i+1], [line[l], line[l]], color=colors[j])

        oldValues = np.copy(values)

        ax.plot([i, i+1], [np.sum(values), np.sum(values)], color='gray', linewidth=2, marker='o')
        if oldSum != -1:
            ax.plot([i, i], [oldSum, np.sum(values)], '--', linewidth=1, color='gray')
        oldSum = np.sum(values)
    

    labels.append('Total amount')
    ax.set_title('Flower population and distribution')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('n Flowers')
    ax.legend(labels=labels)
    #help(ax.legend(labels=labels))

def PlotBeePopulation(ax):
    ax.set_title('Bee population')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('n Bees')

def PlotFlowerBeeDensity(ax):
    ax.set_title('Flowers / Bee')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('Flowers / Bee')

def PlotAvgLifespan(ax):
    ax.set_title('Average Lifespan (Bees)')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('Time')

def MergePlots(data):
    print('Enter')
    fig, axs = plt.subplots(2, 2)
    PlotFlowerAmount(axs[0, 0], data)  # Pass individual subplot
    PlotBeePopulation(axs[0, 1])  # Pass individual subplot
    PlotAvgLifespan(axs[1, 1])    # Pass individual subplot
    PlotFlowerBeeDensity(axs[1, 0])  # Pass individual subplot
    plt.show()