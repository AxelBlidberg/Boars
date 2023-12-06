
from Bee import *
from Environment import *
from Result import *

class BeeSimulation():
    def __init__(self, size, numStartingBees, numStartingFlowers, seasonLength, envType='countryside') -> None:
        self.size = size
        self.numStartingBees = numStartingBees
        self.numStartingFlowers = numStartingFlowers
        self.seasonLength = seasonLength
        self.timestep = 1
        self.season = 1

        self.environment = Environment(size,self.seasonLength, envType)
        self.environment.InitializeFlowers(numStartingFlowers)
        self.environment.InitializeBeeNest(numStartingBees)

        self.swarm = Swarm(self.seasonLength)
    
        self.swarm.InitializeBees(numStartingBees, self.environment.nests)

    def CheckBoundaryCollision(self, bee): 
        if 0+5 < bee.x < self.size-5 and 0+5 < bee.y < self.size-5:
            return
        bee.orientation += np.pi/3

    def Update(self):
        self.timestep += 1 
        self.swarm.PushUpdate(self.environment.flowers, self.timestep)
        self.environment.PushUpdate(self.timestep)
        
        if self.timestep % self.seasonLength ==0:
            self.season += 1
            print(f"season {self.season}")

            self.environment.newNests = self.swarm.newNests
            self.environment.CreateNewGeneration(self.timestep)
            self.swarm.CreateNewGeneration(self.timestep, self.environment.nests)

        if len(self.swarm.bees) == 0: # Jump in time if no bees
            self.timestep = (self.season+1) * self.seasonLength 
            print(f"season{self.season}")
             
        for bee in self.swarm.activeBees:
            self.CheckBoundaryCollision(bee)
