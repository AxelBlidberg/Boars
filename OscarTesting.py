from Simulation import *
from Simulation2 import *
from Result import *
from StochasticEvaluation import *
#import pandas as pd
#from itertools import zip_longest
#import copy

seasonLength = 5000
numStartingFlowers = 4000
numStartingBees = 20
nSeasons = 5
num_simulations = 1

blueprint = BeeSim(size=1000, num_bees=numStartingBees, num_flowers=numStartingFlowers, envType='countryside', beeDist = 'dummy', NumSeason=nSeasons, seasonLength=seasonLength)

SaveSimulation('simulations.pkl', blueprint)

sim = LoadSimulation('simulations.pkl', 1)

flowerData, beeData, lifespanData, eggsData, visitedFlowers, bee_types, beeDataHistory, fbRatio,pollenData = sim.RunSimulation()

max_length = max(len(flowerData), len(beeData), len(lifespanData), len(eggsData), len(visitedFlowers), len(bee_types), len(beeDataHistory), len(fbRatio))

MergePlots(flowerData, beeData, lifespanData, eggsData, visitedFlowers, bee_types,beeDataHistory, fbRatio,pollenData)
