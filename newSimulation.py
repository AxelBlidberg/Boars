
from Bee import *
from Environment import *
from Result import *

class BeeSimulation():
    def __init__(self, size, numStartingBees, numStartingFlowers, seasonLength, envType='countryside') -> None:
        self.size = size
        self.numStartingBees = numStartingBees
        self.numStartingFlowers = numStartingFlowers
        self.seasonLength = seasonLength
        self.timestep = 0

        self.environment = Environment(size,self.seasonLength, envType)
        self.environment.InitializeFlowers(numStartingFlowers)
        self.environment.InitializeBeeNest(numStartingBees)

        self.swarm = Swarm(self.seasonLength)
    
        self.swarm.InitializeBees(numStartingBees, self.environment.nests)

        # Plot data
        self.currentFData = []
        self.flowerData = []
        self.currentBData = []
        self.beeData = []
        self.currentLData = []
        self.lifespanData = []

    def CheckBoundaryCollision(self, bee): 
        if 0+5 < bee.x < self.size-5 and 0+5 < bee.y < self.size-5:
            return
        bee.orientation += np.pi/3

    def Update(self):
        self.timestep += 1 
        self.swarm.PushUpdate(self.environment.flowers, self.timestep)

        if len(self.swarm.bees) == 0: # Jump in time if no bees
            self.timestep = (self.season+1) * self.seasonLength 
             
        for bee in self.swarm.activeBees:
            self.CheckBoundaryCollision(bee)
    
        if self.timestep % 0.25*self.seasonLength == 0:
            self.currentFData.append(self.environment.FlowerDistribution())
            self.currentBData.append(self.swarm.BeeDistribution())
        if self.timestep % self.seasonLength == 0:
            self.flowerData.append(np.copy(self.currentFData))
            self.currentFData = []
            self.beeData.append(np.copy(self.currentBData))
            self.currentBData = []

        if self.timestep % 10*self.seasonLength == 0:
            MergePlots(self.flowerData, self.beeData, self.lifespanData)



        
