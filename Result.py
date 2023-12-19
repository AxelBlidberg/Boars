import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os, csv
import pandas as pd
import seaborn as sns

def SaveData(data, filename):
    '''
    Temporary file for saving data to CSV for finding problems in the data sent from the Simulation file
    '''
    folder = 'Data'
    filePath = os.path.join(os.getcwd(), folder, filename)
    with open(filePath, 'w', newline='') as file:
        writer=csv.writer(file)
        writer.writerows(data)

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
    x = np.arange(0, len(fData)/0.25, step=0.25)
    x = np.linspace(0, len(fData), num=(4*len(fData)+1)) # remove +1?
    x = x[:-1]

    for i in range(len(trends)):
        ax2.plot(x, trends[i], color=colors[i])
    ax1.plot(x, amount, color='gray')

    ax1.set_title('Total flower amount')
    ax1.set_xlabel('Seasons')
    ax1.set_ylabel('n Flowers')
    ax2.set_title('Flower distribution')
    ax2.set_xlabel('Seasons')
    ax2.set_ylabel('n Flowers')
    ax2.legend(labels=labels, loc='center left', bbox_to_anchor=(1, 0.75))
    return x

def PlotPollenAmount(ax1, ax2, fData):
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
    x = np.arange(0, len(fData)/0.25, step=0.25)
    x = np.linspace(0, len(fData), num=(4*len(fData)+1)) # remove +1?
    x = x[:-1]

    for i in range(len(trends)):
        ax2.plot(x, trends[i], color=colors[i])
    ax1.plot(x, amount, color='gray')

    ax1.set_title('Total pollen amount')
    ax1.set_xlabel('Seasons')
    ax1.set_ylabel('n Flowers')
    ax2.set_title('Pollen distribution')
    ax2.set_xlabel('Seasons')
    ax2.set_ylabel('n Flowers')
    ax2.legend(labels=labels, loc='center left', bbox_to_anchor=(1, 0.75))
    return x

def PlotBeePopulation(ax1, ax2, bData, x):
    labels = ['Small Bee', 'Intermediate Bee', 'Bee population']
    colors = ['blue', 'red', 'gray']
    trends = [[], [], []]
    amount = []

    for i, season in enumerate(bData):
        for j, quarter in enumerate(season):
            values = []
            for k in range(len(labels)-1):
                values.append(quarter[k])
                trends[k].append(quarter[k])
            trends[2].append(np.sum(values))
            amount.append(np.sum(values))
    
    ax1.plot(x, trends[-1], color=colors[-1], label=labels[-1])
    ax2.plot(x, trends[0], color=colors[0], label=labels[0])
    ax2.plot(x, trends[1], color=colors[1], label=labels[1])
    

    ax1.set_title('Bee population')
    ax1.set_xlabel('Seasons')
    ax1.set_ylabel('n.o. Bees')

    ax2.set_title('Bee type distribution')
    ax2.set_xlabel('Seasons')
    ax2.set_ylabel('n.o. Bees')
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.9))

def PlotFlowerBeeDensity(ax, r):
    x = np.linspace(0, len(r), num=len(r))
    ax.plot(x, r)
    ax.set_title('Flowers / Bee')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('Flowers / Bee')

def PlotAvgLifespan(ax,smallBeeData,mediumBeeData):
    #Convert to boxplot
    if len(smallBeeData) > len(mediumBeeData):
        ticks = np.arange(0,len(smallBeeData))
    else: 
        ticks = np.arange(0,len(mediumBeeData))
    
    ax.boxplot(smallBeeData)
    #ax.boxplot(mediumBeeData)
    ax.set_xticklabels(ticks)
    ax.set_title('Average Lifespan (Bees)')
    ax.set_xlabel('Seasons')
    ax.set_ylabel('Time')

def SeparateTypes(beeDistributionHistory, lifespanData, eggsData,visitedFlowers, bee_types, ax1, ax2, ax3):

    data = {'lifespanData': lifespanData, 'eggsData': eggsData, 'visitedFlowers': visitedFlowers,'bee_types': bee_types, 'generation': beeDistributionHistory}
    folder = 'Data'
    filePath = os.path.join(os.getcwd(), folder, 'test.csv')
    df = pd.DataFrame(data)
    df.to_csv(filePath, index=False)

    df['visitedFlowersPerDay'] = df['visitedFlowers'] / df['lifespanData']

    sns.boxplot(x='generation', y='eggsData', data=df, hue="bee_types", width=0.6, ax=ax1)
    ax1.set_title('Box Plot of eggsData')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('eggsData')

    sns.boxplot(x='generation', y='visitedFlowersPerDay', data=df, hue="bee_types", width=0.6, ax=ax2)
    ax2.set_title('Box Plot of visitedFlowers')
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('visitedFlowers')

    sns.boxplot(x='generation', y='lifespanData', data=df, hue="bee_types", width=0.6, ax=ax3)
    ax3.set_title('Box Plot of lifespanData')
    ax3.set_xlabel('Generation')
    ax3.set_ylabel('lifespanData')

def MergePlots(flowerData, beeDistribution, lifespanData, eggsData, visitedFlowers, bee_types,beeDistributionHistory, fbRatio,pollenData):
    #SaveData(flowerData, 'fData.csv')
    #SaveData(beeDistribution, 'bData.csv')
    fig, axs = plt.subplots(3, 3, gridspec_kw={'hspace': 0.5, 'wspace': 0.75})
    x = PlotFlowerAmount(axs[0, 0], axs[1,0], flowerData)  # Pass individual subplot
    PlotBeePopulation(axs[0, 1], axs[1,1], beeDistribution, x)  # Pass individual subplot
    #PlotFlowerBeeDensity(axs[2, 1], fbRatio)  # Pass individual subplot
    PlotPollenAmount(axs[2,0], axs[2,1], pollenData)
    SeparateTypes(beeDistributionHistory, lifespanData, eggsData,visitedFlowers, bee_types, axs[0, 2], axs[1, 2], axs[2, 2])
    # axs[2,0] sparad till clustering coefficient, axels plot
    #axs[2,0].set_title('Clustering coefficient')

    plt.show()
