import numpy as np
from tqdm import tqdm
from Bee import *
from Environment import *
from Result import *
import time

class BeeSim:
    def __init__(self, size=1000, num_bees=4, num_flowers=1500, envType='countryside', NumSeason=10, seasonLength=5000):
        # Initialize simulation parameters
        self.size = size
        self.num_flowers = num_flowers
        self.seasonLength = seasonLength
        self.timestep = 0
        self.season = 1
        self.simulationLength = NumSeason
        self.SimulationBar = tqdm(total=self.simulationLength * self.seasonLength, desc="Simulation progress", unit=" Time steps")
        self.seasonStartTime = time.time()

        # Initialize environment and swarm
        self.environment = Environment(size, self.seasonLength, envType)
        self.environment.InitializeFlowers(num_flowers)
        self.environment.InitializeBeeNest(num_bees)
        
        self.swarm = Swarm(self.seasonLength)
        self.swarm.InitializeBees(num_bees, self.environment.nests, self.timestep)
        
    def Update(self):
        self.timestep += 1
        if self.timestep % self.seasonLength == 0:
            self.SimulationBar.write(f'Time to simulate season {self.season}: {(time.time() - self.seasonStartTime)//60:2.0f} minutes and {(time.time() - self.seasonStartTime)%60:2.0f} seconds')
            self.seasonStartTime = time.time()
            self.environment.newNests = self.swarm.newNests
            self.environment.CreateNewGeneration(self.timestep)
            self.swarm.CreateNewGeneration(self.timestep, self.environment.nests)
            self.season += 1

        self.swarm.PushUpdate(self.environment.flowers, self.timestep)
        self.environment.PushUpdate(self.timestep)
        self.SimulationBar.update(1)

    def RunQuarter(self, quarter):
        # Simulate one quarter of the season
        for _ in range(int(0.25 * self.seasonLength)):
            self.timestep += 1
            self.swarm.PushUpdate(self.environment.flowers, self.timestep)
            self.environment.PushUpdate(self.timestep)
            self.SimulationBar.update(1)

    def RunSimulation(self):
        quarters = [1, 2, 3, 4]
        startTime = time.time()

        for season in range(self.simulationLength):
            seasonStartTime = time.time()
            # Create new generation
            if season > 0:
                self.environment.newNests = self.swarm.newNests
                self.environment.CreateNewGeneration(self.timestep)
                self.swarm.CreateNewGeneration(self.timestep, self.environment.nests)

            for quarter in quarters:
                # Run each quarter
                self.RunQuarter(quarter)
                #SimulationBar.update(self.seasonLength/4)
                
            self.season += 1
            self.SimulationBar.write(f'Time to simulate season {self.season}: {(time.time() - seasonStartTime)//60:2.0f} minutes and {(time.time() - seasonStartTime)%60:2.0f} seconds')

        self.SimulationBar.close()
        print(f'Simulation time: {(time.time() - startTime)//60:2.0f} minutes and {(time.time() - startTime)%60:2.0f} seconds')

if __name__ == "__main__":
    # Example usage
    simulation = BeeSim()
    simulation.RunSimulation()
