from Environment import *
import numpy as np
import matplotlib.pyplot as plt

def PlotFunction(data):
    '''
    Temporary function for plotting the environment. Takes a special formatted list obtained from the ExportContent method in the Environment class.
    '''
    figure, axs = plt.subplots(1, 4)
    times = [0, 500, 1000, 1500]

    for i in range(4):
        types = [item[1] for item in data[i]]
        x_values = [item[2] for item in data[i]]
        y_values = [item[3] for item in data[i]]
        unique_types = set(types)
        color_map = {t: i for i, t in enumerate(unique_types)}
        colors = [color_map[t] for t in types]
        axs[i].scatter(x_values, y_values, c=colors, cmap='viridis', s=50, alpha=0.8, label=types)
        axs[i].set_xlabel('X-axis')
        axs[i].set_ylabel('Y-axis')
        axs[i].set_xlim([0, 1000])
        axs[i].set_ylim([0, 1000])
        axs[i].set_title(f'Flowers at timestep: {times[i]}')
    plt.show()

env = Environment(1000)
env.InitializeFlowers(100, 0)

time = np.linspace(0, 1600, 1601, dtype=int)
data = []
for t in time:
    env.PushUpdate(t)

    if t % 200 == 0 and t != 0:
        p = np.random.randint(0, len(env.flowers))
        env.flowers[p].pollen += 1002

    if t % 505 == 0:
        data.append(env.ExportContent())
        print(len(data[-1]), t)
        dist = env.FlowerDistribution()
        print(dist)



PlotFunction(data)


