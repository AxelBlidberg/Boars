import numpy as np
import matplotlib.pyplot as plt

class ResultVisualisation():
    def __init__(self) -> None:

        # Plotting data
        self.flowerData = []
        self.beePopulationData = []
        self.beeLifespanData = []

    def ConstructPlot(self):
        fig, axs = plt.subplots(2, 2, gridspec_kw={'hspace': 0.5, 'wspace': 0.5})
        self.PlotFlowerAmount(axs[0, 0], self.flowerData)  # Pass individual subplot
        self.PlotBeePopulation(axs[0, 1], self.beePopulationData)  # Pass individual subplot
        self.PlotAvgLifespan(axs[1, 1])    # Pass individual subplot
        self.PlotFlowerBeeDensity(axs[1, 0], self.beePopulationData)  # Pass individual subplot
        plt.show()

    def PlotFlowerAmount(self, ax):
        labels = ['Lavender', 'Bee balm', 'Sunflower', 'Coneflower', 'Blueberry']
        colors = ['purple', 'red', 'orange', 'pink', 'blue']
        oldSum = -1

        for i, line in enumerate(self.flowerData):
            values = []
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

    def PlotFlowerBeeDensity(self, ax):
        ax.set_title('Flowers / Bee')
        ax.set_xlabel('Seasons')
        ax.set_ylabel('Flowers / Bee')

    def PlotBeePopulation(self, ax):
        ax.set_title('Bee population')
        ax.set_xlabel('Seasons')
        ax.set_ylabel('n Bees')

    def PlotAvgLifespan(self, ax):
        ax.set_title('Average Lifespan (Bees)')
        ax.set_xlabel('Seasons')
        ax.set_ylabel('Time')

    def UpdatePlots(self, fData, bData, lData):
        self.flowerData.append(fData)
        self.beePopulationData.append(bData)
        self.beeLifespanData.append(lData)

        self.ConstructPlot()

