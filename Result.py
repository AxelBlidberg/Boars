import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def PlotFlowerAmount(ax, data):
    labels = ['Lavender', 'Bee balm', 'Sunflower', 'Coneflower', 'Blueberry']
    colors = ['purple', 'red', 'orange', 'pink', 'blue']
    encoding = [1, 2, 3, 4, 5]

    for i, generation in enumerate(data):
        counter = [[c+1, 0] for c in encoding]
        types = [flower[1] for flower in generation]

        for c in range(len(counter)):
            for j in range(len(types)):
                if types[c] == counter[c][0]:
                    counter[c][1] += 1
        print(counter)
        
        for c in range(len(counter)):
            ax.plot([i, i+1], [counter[c][1], counter[c][1]], color=colors[c])

        ax.plot([i, i+1], [len(types), len(types)], color='gray')

    ax.set_title('Flower population and distribution')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('n Flowers')

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
