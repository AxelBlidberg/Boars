import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os, csv
import pandas as pd
import seaborn as sns

def SaveData(data, filename):
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
    return x, amount

def PlotBeePopulation(ax1, bData, x):
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
    
    for i in range(len(trends)):
        ax1.plot(x, trends[-(i+1)], color=colors[-(i+1)], label=labels[-(i+1)])
    

    ax1.set_title('Bee population')
    ax1.set_xlabel('Seasons')
    ax1.set_ylabel('n Bees')
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.9))
    return amount

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

def SeparateTypes2(beeDistributionHistory, lifespanData, eggsData,visitedFlowers, bee_types, ax1, ax2, ax3):

    data = {'lifespanData': lifespanData, 'eggsData': eggsData, 'visitedFlowers': visitedFlowers,'bee_types': bee_types, 'generation': beeDistributionHistory}

    df = pd.DataFrame(data)
    df.to_csv('test.csv', index=False)

    df['visitedFlowersPerDay'] = df['visitedFlowers'] / df['lifespanData']

    #fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

    sns.boxplot(x='generation', y='eggsData', data=df, hue="bee_types", width=0.6, ax=ax1)
    ax1.set_title('Box Plot of eggsData')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('eggsData')

    sns.boxplot(x='generation', y='visitedFlowersPerDay', data=df, hue="bee_types", width=0.6, ax=ax2)
    ax2.set_title('Box Plot of visitedFlowers')
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('visitedFlowers')

    sns.boxplot(x='generation', y='lifespanData', data=df, hue="bee_types", width=0.6, ax=ax2)
    ax3.set_title('Box Plot of lifespanData')
    ax3.set_xlabel('Generation')
    ax3.set_ylabel('lifespanData')

def SeparateTypes(beeDistributionHistory, lifespanData, eggsData,visitedFlowers, bee_types, axs):
    #Ta ut index för varje typ 
    #Använd de indexen flr att ta ut lifespan, antal egg och visited flowers
    smallBee_eggs =[]
    smallBee_flowers = []
    smallBee_age = []
    
    mediumBee_eggs= []
    mediumBee_flowers = []
    mediumBee_age = []

    for i in range(len(lifespanData)):
        if bee_types[i] == 0:
            smallBee_eggs.append(eggsData[i])
            smallBee_flowers.append(visitedFlowers[i])
            smallBee_age.append(lifespanData[i])
        else:
            mediumBee_eggs.append(eggsData[i])
            mediumBee_flowers.append(visitedFlowers[i])
            mediumBee_age.append(lifespanData[i])

    eggs = np.zeros((2,len(beeDistributionHistory)))
    flowers = np.zeros((2,len(beeDistributionHistory)))
    age = np.zeros((2,len(beeDistributionHistory)))
    
    j = 0
    k = 0
    #print("beeDistributionHistory:",beeDistributionHistory)
    for i,n in enumerate(beeDistributionHistory):
        iSmallBee = n[0]
        iMediumBee = n[1]
        if iSmallBee > 0:
            eggs[0,i] = smallBee_eggs[j:j+iSmallBee[0]]
            flowers[0,i] = smallBee_eggs[j:j+iSmallBee[0]]
            age[0,i] = smallBee_eggs[j:j+iSmallBee[0]]
            j = j + nBees[0]

        if iMediumBee > 0:
            eggs[1,i] = mediumBee_eggs[k:k+nBees[1]]
            flowers[1,i] = mediumBee_eggs[k:k+iMediumBee[1]]
            age[1,i] = mediumBee_eggs[k:k+iMediumBee[1]]
            k = k + iMediumBee[1]

    ax1 = axs[1, 1]
    
    PlotAvgLifespan(ax1,smallBee_age,mediumBee_age)
        
    return smallBee_eggs, smallBee_flowers,smallBee_age,mediumBee_eggs,mediumBee_flowers,mediumBee_age

def BoxPlot(s_eggs,s_flowers,s_age,m_eggs,m_flowers,m_age):
    pass

def MergePlots(flowerData, beeDistribution, lifespanData, eggsData, visitedFlowers, bee_types,beeDistributionHistory, fbRatio):
    SaveData(flowerData, 'fData.csv')
    SaveData(beeDistribution, 'bData.csv')
    #SaveFunction(flowerData, beeDistribution)
    #s_eggs, s_flowers,s_age,m_eggs,m_flowers,m_age = SeparateTypes(beeDistribution, lifespanData, eggsData,visitedFlowers, bee_types)
    fig, axs = plt.subplots(3, 3, gridspec_kw={'hspace': 0.5, 'wspace': 0.75})
    #axs[0, 0].get_shared_x_axes().join(axs[0, 0], axs[1, 0])
    #axs[0, 1].get_shared_x_axes().join(axs[0, 1], axs[1, 1])
    x, fPop = PlotFlowerAmount(axs[0, 0], axs[1,0], flowerData)  # Pass individual subplot
    bPop = PlotBeePopulation(axs[0, 1], beeDistribution, x)  # Pass individual subplot
    #PlotAvgLifespan(axs[1, 1],lifespanData)    # Pass individual subplot
    PlotFlowerBeeDensity(axs[2, 0], fbRatio)  # Pass individual subplot
    #BoxPlot(s_eggs,s_flowers,s_age,m_eggs,m_flowers,m_age)
    SeparateTypes2(beeDistributionHistory, lifespanData, eggsData,visitedFlowers, bee_types, axs[2, 0], axs[2, 1], axs[2, 2])

    #print("BEE distribution history", beeDistributionHistory)

    plt.show()

#MergePlots(fData, bData, [])