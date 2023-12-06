import numpy as np
from Bee import *
from Environment import *
from Result import *

class BeeSimulation():
    def __init__(self, size, numStartingBees, numStartingFlowers, seasonLength, envType='countryside') -> None:
        self.size = size
        self.numStartingBees = numStartingBees
        self.numStartingFlowers = numStartingFlowers
        self.seasonLength = seasonLength
        self.season = 0
        self.timestep = 0

        self.environment = Environment(size,self.seasonLength, envType)
        self.environment.InitializeFlowers(numStartingFlowers)
        self.environment.InitializeBeeNest(numStartingBees)

        self.swarm = Swarm(self.seasonLength)
        self.swarm = Swarm(self.seasonLength)
    
        self.swarm.InitializeBees(numStartingBees, self.environment.nests)

        # Plot data
        self.currentFData = []
        self.flowerData = []
        self.currentBData = []
        self.beeData = []
        self.currentLData = []
        self.lifespanData = []
        self.eggsData = []
        self.visitedFlowers = []
        self.bee_types =[]
        self.beeDistributionHistory =[]

    def CheckBoundaryCollision(self, bee): 
        if 0+5 < bee.x < self.size-5 and 0+5 < bee.y < self.size-5:
            return
        bee.orientation += np.pi/3
    
    def SkipTimeSteps(self):
        TimeJump = lambda multiplier: (self.seasonLength*(int(self.timestep/self.seasonLength))) + multiplier*self.seasonLength
        steps = [TimeJump(0), TimeJump(0.25), TimeJump(0.5), TimeJump(0.75)]
        for iStep in steps:
            nextStep = max(self.timestep, iStep)
            if nextStep > self.timestep: 
                self.timestep = nextStep
                print(f'Data save at timestep: {self.timestep}')
                self.environment.PushUpdate(self.timestep)
                self.currentFData.append(self.environment.FlowerDistribution())
                self.currentBData.append(self.swarm.BeeDistribution(0))
        self.timestep = self.seasonLength*(self.season+1)

    def Update(self):
        self.timestep += 1 
        self.swarm.PushUpdate(self.environment.flowers, self.timestep)

        if len(self.swarm.bees) == 0: # Jump in time if no bees
            #self.timestep = (self.season+1) * self.seasonLength 
            print('All bees died, skip to next season')
            self.SkipTimeSteps()
             
        for bee in self.swarm.activeBees:
            self.CheckBoundaryCollision(bee)
        

        if self.timestep %self.seasonLength ==0 and self.timestep !=0: # Every change of season
            
            self.eggsData = self.swarm.RIP_number_of_eggs
            self.visitedFlowers = self.swarm.RIP_visitedflowers
            self.bee_types = self.swarm.RIP_types
            self.lifespanData = self.swarm.RIP_ages

            self.environment.newNests = self.swarm.newNests
            self.environment.CreateNewGeneration(self.timestep)
            self.swarm.CreateNewGeneration(self.timestep, self.environment.nests)

            self.season += 1

        if self.timestep % (0.25*self.seasonLength) == 0 or self.timestep == 1: # every quarter season: 0.25, 0.5,0.75..
            print(f'Data save at timestep: {self.timestep}')
            self.currentFData.append(self.environment.FlowerDistribution())
            self.currentBData.append(self.swarm.BeeDistribution(0))
            
        if self.timestep % self.seasonLength == 0: # start of every season
            self.flowerData.append(np.copy(self.currentFData))
            self.currentFData = []
            self.beeData.append(np.copy(self.currentBData))
            self.currentBData = []
            

        if self.timestep % (10*self.seasonLength) == 0: # after 10 seasons
            self.beeDistributionHistory = self.swarm.BeeDistribution(1)

            MergePlots(self.flowerData, self.beeData, self.lifespanData, self.eggsData, self.visitedFlowers, self.bee_types,self.beeDistributionHistory)
            


        
