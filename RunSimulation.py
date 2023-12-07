from Simulation2 import *

#Definition av rum
#Grid på 1000 x 1000
#En pixel är 0.2 x 0.2 m i verkligheten total utsträckning på 1 km

#Definition av tid
#Season lenght = 112000
#Vi räknar med att ett bi max lever 8 veckor
#En dag är 2000 tidssteg

#size, numStartingBees, numStartingFlowers, seasonLength,

seasonLength = 5000
numStartingFlowers = 2000
numStartingBees = 20
nSeasons = 4

sim = BeeSim(size=1000, num_bees=20, num_flowers=2000, envType='countryside', NumSeason=nSeasons, seasonLength=seasonLength)
sim.RunSimulation()
