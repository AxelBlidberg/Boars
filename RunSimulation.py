from newSimulation import *

#Definition av rum
#Grid på 1000 x 1000
#En pixel är 0.2 x 0.2 m i verkligheten total utsträckning på 1 km

#Definition av tid
#Season lenght = 112000
#Vi räknar med att ett bi max lever 8 veckor
#En dag är 2000 tidssteg

### Some what stable values:
seasonLength = 5000
numStartingFlowers = 2000
numStartingBees = 20

### For bow plot
#seasonLength = 1000
#numStartingFlowers = 2000
#numStartingBees = 20

beesim = BeeSimulation(1000, numStartingBees, numStartingFlowers,seasonLength)

simulationLength = seasonLength * 4

for i in range(simulationLength): #Defining ho
    beesim.Update()

