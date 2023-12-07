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
    x = np.linspace(0, len(fData), num=(4*len(fData)+1))
    #print(len(fData))
    #print(len(trends))
    #print(len(x), x)
    #print(len(trends[0]))
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
    trends = [[], []]
    amount = []
    #print('Lengths: ', len(bData))
    #for i in bData:
        #print(len(i))

    for i, season in enumerate(bData):
        for j, quarter in enumerate(season):
            values = []
            for k in range(len(labels)-1):
                values.append(quarter[k])
                trends[k].append(quarter[k])
            amount.append(np.sum(values))
    #print('x: ', x)
    #print('Total: ', amount)
    #print('Trends: ', trends)
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

def SeparateTypes2(beeDistributionHistory, lifespanData, eggsData,visitedFlowers, bee_types):

    data = {'lifespanData': lifespanData, 'eggsData': eggsData, 'visitedFlowers': visitedFlowers,'bee_types': bee_types, 'generation': beeDistributionHistory}

    df = pd.DataFrame(data)
    df.to_csv('test.csv', index=False)

    df_smallBee = df[df['bee_types'] == 0]
    df_LargeBee = df[df['bee_types'] == 1]

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

    # Box plot for eggsData
    sns.boxplot(x='generation', y='eggsData', data=df_smallBee, width=0.6, ax=axes[0])
    sns.boxplot(x='generation', y='eggsData', data=df_LargeBee, width=0.6, ax=axes[0])
    axes[0].set_title('Box Plot of eggsData')
    axes[0].set_xlabel('Generation')
    axes[0].set_ylabel('eggsData')

    # Box plot for visitedFlowers
    sns.boxplot(x='generation', y='visitedFlowers', data=df_smallBee, width=0.6, ax=axes[1])
    sns.boxplot(x='generation', y='visitedFlowers', data=df_LargeBee, width=0.6, ax=axes[1])
    axes[1].set_title('Box Plot of visitedFlowers')
    axes[1].set_xlabel('Generation')
    axes[1].set_ylabel('visitedFlowers')

    # Box plot for lifespanData
    sns.boxplot(x='generation', y='lifespanData', data=df_smallBee, width=0.6, ax=axes[2])
    sns.boxplot(x='generation', y='lifespanData', data=df_LargeBee, width=0.6, ax=axes[2])
    axes[2].set_title('Box Plot of lifespanData')
    axes[2].set_xlabel('Generation')
    axes[2].set_ylabel('lifespanData')

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()
    #print(df_smallBee)
    #print(beeDistributionHistory)


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
            j = j + iSmallBee[0]

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

def MergePlots(flowerData, beeDistribution, lifespanData, eggsData, visitedFlowers, bee_types,beeDistributionHistory):
    SaveData(flowerData, 'fData.csv')
    SaveData(beeDistribution, 'bData.csv')
    #SaveFunction(flowerData, beeDistribution)
    #s_eggs, s_flowers,s_age,m_eggs,m_flowers,m_age = SeparateTypes(beeDistribution, lifespanData, eggsData,visitedFlowers, bee_types)
    #axs[0, 0].get_shared_x_axes().join(axs[0, 0], axs[1, 0])
    #axs[0, 1].get_shared_x_axes().join(axs[0, 1], axs[1, 1])
        
    #PlotAvgLifespan(axs[1, 1],lifespanData)    # Pass individual subplot
    #BoxPlot(s_eggs,s_flowers,s_age,m_eggs,m_flowers,m_age)
    

    #PlotFlowerBeeDensity(axs[2, 0], fPop, bPop, x)  # Pass individual subplot
    SeparateTypes2(beeDistributionHistory, lifespanData, eggsData,visitedFlowers, bee_types)

    #fig, axs = plt.subplots(3, 3, gridspec_kw={'hspace': 0.5, 'wspace': 0.75})
    #x, fPop = PlotFlowerAmount(axs[0, 0], axs[1,0], flowerData)  # Pass individual subplot
    #bPop = PlotBeePopulation(axs[0, 1], beeDistribution, x)  # Pass individual subplot

    #print("BEE distribution history", beeDistributionHistory)
    #print("BEE distribution history", flowerData)

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