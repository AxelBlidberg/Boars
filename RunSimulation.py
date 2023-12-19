from Simulation import *
#from Simulation2 import *
from Result import *
import pandas as pd
from itertools import zip_longest

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
num_simulations = 1

# Run simulations in a loop
for i in range(0,num_simulations):
    print("Simulation", i , "Began")
    sim = BeeSim(size=1000, num_bees=numStartingBees, num_flowers=numStartingFlowers, envType='countryside', beeDist = 'dummy', NumSeason=nSeasons, seasonLength=seasonLength)
    
    flowerData, beeData, lifespanData, eggsData, visitedFlowers, bee_types, beeDataHistory, fbRatio,pollenData = sim.RunSimulation()

    max_length = max(len(flowerData), len(beeData), len(lifespanData), len(eggsData), len(visitedFlowers), len(bee_types), len(beeDataHistory), len(fbRatio))

"""
    # Pad or truncate each column to match the maximum length
    flowerData += [None] * (max_length - len(flowerData))
    beeData += [None] * (max_length - len(beeData))
    lifespanData += [None] * (max_length - len(lifespanData))
    eggsData += [None] * (max_length - len(eggsData))
    visitedFlowers += [None] * (max_length - len(visitedFlowers))
    bee_types += [None] * (max_length - len(bee_types))
    beeDataHistory += [None] * (max_length - len(beeDataHistory))
    fbRatio += [None] * (max_length - len(fbRatio))

    df = pd.DataFrame({
    'flowerData': flowerData,
    'beeData': beeData,
    'lifespanData': lifespanData,
    'eggsData': eggsData,
    'visitedFlowers': visitedFlowers,
    'bee_types': bee_types,
    'beeDataHistory': beeDataHistory,
    'fbRatio': fbRatio })

    df.to_csv('output_' + str(i) + '.csv', index=False)
# Save DataFrame to a CSV file
"""

#print(bee_types)
MergePlots(flowerData, beeData, lifespanData, eggsData, visitedFlowers, bee_types,beeDataHistory, fbRatio,pollenData)


"""

df = pd.DataFrame({
    'flowerData': flowerData,
    'beeData': beeData,
    'lifespanData': lifespanData,
    'eggsData': eggsData,
    'visitedFlowers': visitedFlowers,
    'bee_types': bee_types,
    'beeDataHistory': beeDataHistory,
    'fbRatio': fbRatio
})

# Save DataFrame to a CSV file
df.to_csv('output.csv', index=False)


#sim = BeeSim(size=1000, num_bees=numStartingBees, num_flowers=numStartingFlowers, envType='countryside', NumSeason=nSeasons, seasonLength=seasonLength)
#sim.RunSimulation()

#simV = BeeSimV(size=1000, num_bees=numStartingBees, num_flowers=numStartingFlowers, envType='countryside', NumSeason=nSeasons, seasonLength=seasonLength)
#simV.RunSimulation()

"""