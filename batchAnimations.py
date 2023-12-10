import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from standaloneSimulation import *

def run_simulation(params):
    beesim = BeeSim(**params)
    fig, ax = plt.subplots(figsize=(8, 8))

    def update(frame, params):
        beesim.SimulationBar.write(f'{len(beesim.swarm.bees)} Bees')
        if len(beesim.swarm.bees) > 300:
            beesim.SimulationBar.write('Bee population explosion limit')
            return
        
        if frame > 0:
            for _ in range(params['seasonLength']):
                beesim.Update()

        flower_positions = np.array([[flower.x, flower.y] for flower in beesim.environment.flowers])
        nest_positions = np.array([[nest.x, nest.y] for nest in beesim.environment.nests])

        ax.clear()
        ax.scatter(flower_positions[:, 0], flower_positions[:, 1], marker='.', label='Flowers') if len(flower_positions > 0) else print("No flowers")
        ax.scatter(nest_positions[:, 0], nest_positions[:, 1], marker='s', s=25, label='Nests') if len(nest_positions > 0) else print("No nests")

        ax.set_xlim(0, params['size'])
        ax.set_ylim(0, params['size'])
        ax.set_xticks([])
        ax.set_yticks([])

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
                  ncol=2, fancybox=True, shadow=True)

        ax.set_title(f'Season {beesim.season}')

    ani = FuncAnimation(fig, update, frames=params['NumSeason'], fargs=(params,), repeat=True, interval=1000)

    ani.save(f'GIFs/S{i}_SLen{params["seasonLength"]}_B{params["num_bees"]}F{params["num_flowers"]}.gif')


simulation_params = [
    {'size': 1000, 'num_bees': 2, 'num_flowers': 2000, 'envType': 'countryside', 'NumSeason': 20, 'seasonLength': 10000},
    {'size': 1000, 'num_bees': 8, 'num_flowers': 1500, 'envType': 'countryside', 'NumSeason': 20, 'seasonLength': 5000},
    {'size': 1000, 'num_bees': 10, 'num_flowers': 2500, 'envType': 'countryside', 'NumSeason': 20, 'seasonLength': 5500},
    {'size': 1000, 'num_bees': 10, 'num_flowers': 1800, 'envType': 'countryside', 'NumSeason': 20, 'seasonLength': 5000},
    {'size': 1000, 'num_bees': 20, 'num_flowers': 2200, 'envType': 'countryside', 'NumSeason': 20, 'seasonLength': 5000}
]

for i , params in enumerate(simulation_params):
    run_simulation(params)
