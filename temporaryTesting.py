from Environment import *
import numpy as np
import matplotlib.pyplot as plt

def PlotFunction(data):
    '''
    Temporary function for plotting the environment. Takes a special formatted list obtained from the ExportContent method in the Environment class.
    '''
    figure, axs = plt.subplots(1, 2)
    times = [0, 500, 1000, 1500]

    for i in range(2):
        types = [item[1] for item in data[i]]
        x_values = [item[2] for item in data[i]]
        y_values = [item[3] for item in data[i]]
        unique_types = set(types)
        color_map = {t: i for i, t in enumerate(unique_types)}
        colors = [color_map[t] for t in types]
        axs[i].scatter(x_values, y_values, c=colors, cmap='viridis', s=50, alpha=0.8, label=types)
        axs[i].set_xlabel('X-axis')
        axs[i].set_ylabel('Y-axis')
        #axs[i].set_xlim([0, 1000])
        #axs[i].set_ylim([0, 1000])
        axs[i].set_title(f'Flowers version: {i}')
    plt.show()

env1 = Environment(100, 'agriculture')
env1.InitializeFlowers(100)
print(len(env1.flowers))
env2 = Environment(1000, 'agriculture')
env2.InitializeFlowers(500)

data = [env1.ExportContent(), env2.ExportContent()]
PlotFunction(data)



