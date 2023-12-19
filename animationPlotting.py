import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from standaloneSimulation import *

def update(frame):
    beesim.SimulationBar.write(f'{len(beesim.swarm.bees)} Bees')
    if len(beesim.swarm.bees) > 100:
        beesim.SimulationBar.write('Bee population explosion limit')
        return
    
    if frame > 0:
        for _ in range(seasonLength):
            beesim.Update()

    flower_positions = np.array([[flower.x, flower.y] for flower in beesim.environment.flowers])
    nest_positions = np.array([[nest.x, nest.y] for nest in beesim.environment.nests])
    #print(f"flowers at: {flower_positions}")
    #print(f"nests at: {nest_positions}")

    ax.clear()
    ax.scatter(flower_positions[:, 0], flower_positions[:, 1], marker='.', label='Flowers') if len(flower_positions>0) else print("No flowers")
    ax.scatter(nest_positions[:, 0], nest_positions[:, 1], marker='s', s=25, label='Nests') if len(nest_positions>0) else print("No nests")

    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_xticks([])
    ax.set_yticks([])
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
        ncol=2, fancybox=True, shadow=True)
    
    ax.set_title(f'Season {beesim.season}')


size = 1000
seasonLength = 5000
numStartingFlowers = 4000
numStartingBees = 20
NumSeason = 5


beesim = BeeSim(size, numStartingBees, numStartingFlowers, 'countryside', NumSeason, seasonLength)

fig, ax = plt.subplots(figsize=(8, 8))

ani = FuncAnimation(fig, update, frames=NumSeason, repeat=True, interval=1000)

ani.save(f'GIFs/S{NumSeason}_SLen{seasonLength}_B{numStartingBees}F{numStartingFlowers}.gif')


