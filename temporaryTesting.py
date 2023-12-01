from Environment import *
from Result import *
<<<<<<< Updated upstream
=======
from Bee import *
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
def RunSimulation(environment):
=======
def RunSimulationFlowers(environment):
>>>>>>> Stashed changes
    data = []
    time = 0
    environment.InitializeFlowers(100)

    for i in range(55):
        time += 101
<<<<<<< Updated upstream
        repro = int(0.1*len(environment.flowers))
=======
        repro = int(0.15*len(environment.flowers))
>>>>>>> Stashed changes

        for i in range(repro):
            j = np.random.randint(0, len(environment.flowers))
            environment.flowers[j].reproduce = True
        environment.PushUpdate(time)

        if time %505 == 0:
            data.append(environment.FlowerDistribution())
        
        if time > 1000 and time < 1100:
<<<<<<< Updated upstream
            environment.CreateNewGeneration(time)
        elif time > 2000 and time < 2100:
            environment.CreateNewGeneration(time)
        elif time > 3000 and time < 3100:
            environment.CreateNewGeneration(time)
        elif time > 4000 and time < 4100:
            environment.CreateNewGeneration(time)

    print('Fake simulation finnished')
    MergePlots(data)

def AgricultureTest():
    env1 = Environment(100, 'agriculture')
    env1.InitializeFlowers(100)
    print(len(env1.flowers))
=======
            environment.CreateNewGeneration(time, [])
        elif time > 2000 and time < 2100:
            environment.CreateNewGeneration(time, [])
        elif time > 3000 and time < 3100:
            environment.CreateNewGeneration(time, [])
        elif time > 4000 and time < 4100:
            environment.CreateNewGeneration(time, [])

    MergePlots(data)

def RunSimulation():
    env = Environment(1000)
    env.InitializeFlowers(200)
    env.InitializeBeeNest(15)

    colony = Swarm()
    colony.InitializeBees(15, env.nests)

    fData = []
    bData = []
    time = 0

    for i in range(55):
        time += 101

        # Update flowers:
        repro = int(0.15*len(env.flowers))

        for i in range(repro):
            j = np.random.randint(0, len(env.flowers))
            env.flowers[j].reproduce = True
        env.PushUpdate(time)

        if time %505 == 0:
            fData.append(env.FlowerDistribution())
            bData.append(len(colony.bees))
        
        if time > 1000 and time < 1100:
            env.CreateNewGeneration(time, [])
            env.AddBeeNest([100,100], 50)
            colony.AddBee(env.nests[-1], time)
        elif time > 2000 and time < 2100:
            env.CreateNewGeneration(time, [])
            env.AddBeeNest([200,100], 50)
            colony.AddBee(env.nests[-1], time)
        elif time > 3000 and time < 3100:
            env.CreateNewGeneration(time, [])
            env.AddBeeNest([300,100], 50)
            colony.AddBee(env.nests[-1], time)
        elif time > 4000 and time < 4100:
            env.CreateNewGeneration(time, [])
            env.AddBeeNest([400,100], 50)
            colony.AddBee(env.nests[-1], time)

    MergePlots(fData, bData)


def AgricultureTest():
    env1 = Environment(100, 'agriculture')
    env1.InitializeFlowers(100)
>>>>>>> Stashed changes
    env2 = Environment(1000, 'agriculture')
    env2.InitializeFlowers(500)
    data = [env1.ExportContent(), env2.ExportContent()]
    PlotFunction(data)


<<<<<<< Updated upstream
env = Environment(1000, 'countryside')
RunSimulation(env)
=======
env = Environment(1000, 'agriculture')
RunSimulationFlowers(env)
>>>>>>> Stashed changes



