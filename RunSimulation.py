from Simulation import *
#from Simulation2 import *
from StochasticEvaluation import *
from Result import *
import pandas as pd
from itertools import zip_longest
import json
import os

#Definition av rum
#Grid på 1000 x 1000
#En pixel är 0.2 x 0.2 m i verkligheten total utsträckning på 1 km

#Definition av tid
#Season lenght = 112000
#Vi räknar med att ett bi max lever 8 veckor
#En dag är 2000 tidssteg

#size, numStartingBees, numStartingFlowers, seasonLength,

seasonLength = 5000 
numStartingFlowers = 4000
numStartingBees = 20
nSeasons = 5

# Set the number of simulations
num_simulations = 10

dataTotalFlower = []
dataTotalPollen = []
dataFlower = [[], [], [], [], []]
dataPollen = []
dataBee = []
dataSimulation = []

directory_path = 'data_json/'

if not os.path.exists(directory_path):
    os.makedirs(directory_path)

blueprint = BeeSim(size=1000, num_bees=numStartingBees, num_flowers=numStartingFlowers, envType='countryside', beeDist = 'dummy', NumSeason=nSeasons, seasonLength=seasonLength)

SaveSimulation('simulations.pkl', blueprint)

# Run simulations in a loop
for i in range(0,num_simulations):
    print("Simulation", i , "Began")
    #sim = BeeSim(size=1000, num_bees=numStartingBees, num_flowers=numStartingFlowers, envType='countryside', beeDist = 'dummy', NumSeason=nSeasons, seasonLength=seasonLength)
    sim = LoadSimulation('simulations.pkl', 1)

    flowerData, beeData,pollenData = sim.RunSimulation()

    data_dict = {}
    for j in range(0,nSeasons):
        data_subdict = {"flowerdata": flowerData[j],
                     "pollendata": pollenData[j],
                     "beedata": beeData[j]}
        
        data_dict[f"season_{j}"] = data_subdict

    file_name = f'dataSimulation_{i}.json'

    file_path = os.path.join(directory_path, file_name)

    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=2)
    

#MergePlots(flowerData, beeData,pollenData)


