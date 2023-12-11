import tkinter as tk
import numpy as np
from tqdm import tqdm
from tkinter import Scale
from Bee import *
from Environment import *
from Result import *
import matplotlib.pyplot as plt
import time


class BeeSimV(tk.Tk):
    def __init__(self, size=1000, num_bees=4, num_flowers=200, envType='countryside', beeDist = 'random', visualize=False, NumSeason=10, seasonLength=1000):
        super().__init__()
        # Define grid and start simulation
        self.size = size
        self.num_flowers = num_flowers
        self.num_bees = num_bees
        self.seasonLength = seasonLength #112000
        self.envType = envType
        self.timestep = 0
        self.season = 0
        self.visualize = visualize
        self.simulationLength = NumSeason
        self.beeDist = beeDist

        #for plot
        self.flowersPlot = []
        self.beesPlot = []

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
        self.beeDataHistory = []
        self.fbRatio = [num_flowers/num_bees]

        if self.visualize:
            self.visualizationSetup()

        self.simulationSetup()


    def visualizationSetup(self):
        
        self.title("Bee Simulation")
        
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side="left", padx=10)
        self.canvas = tk.Canvas(self.canvas_frame, width=self.size, height=self.size, bg='#355E3B')
        self.canvas.pack()

        # Frame for sliders
        self.slider_frame = tk.Frame(self)
        self.slider_frame.pack(side="right", padx=10)

        self.show_vision_var = tk.BooleanVar(value=True)
        self.draw_vision_checkbox = tk.Checkbutton(self.slider_frame, text="Draw Vision", variable=self.show_vision_var, onvalue=True, offvalue=False)
        self.draw_vision_checkbox.pack(pady=5)

    def visualizationUpdate(self):
        self.canvas.delete('all')
        self.title(f"Bee Simulation - time: {self.timestep} | season: {self.season}")
        self.DrawEnvironment()
        for bee in self.swarm.activeBees:
            self.CheckBoundaryCollision(bee)
            self.DrawBee(bee)
            self.DrawPath(bee)
            if self.show_vision_var.get():
                self.DrawVisionField(bee)
        
        self.update()

    def simulationSetup(self):
        self.environment = Environment(self.size, self.seasonLength, self.envType)
        self.environment.InitializeFlowers(self.num_flowers)
        self.environment.InitializeBeeNest(self.num_bees)
        
        self.swarm = Swarm(self.seasonLength)
        self.swarm.InitializeBees(self.num_bees, self.environment.nests,self.beeDist)

    def simulationUpdate(self):
        pass

    def runVisualization(self):
        pass

    #def runSimulation(self):
        #pass


        
    def DrawEnvironment(self):
        
        flower_size = 3
        
        for flower in self.environment.flowers:
            x, y = flower.x, flower.y
            self.canvas.create_oval(x - flower_size, y - flower_size, x + flower_size, y + flower_size, fill=flower.color)
        
        nest_size = 3
        
        for nest in self.environment.nests:
            x, y = nest.x, nest.y
            self.canvas.create_rectangle(x - nest_size, y - nest_size, x + nest_size, y + nest_size, fill=nest.color)
        
        #self.environment.PushUpdate(self.timestep)
        
    def DrawBee(self, bee):
        x, y = bee.x, bee.y
        bee_size = 4
        self.canvas.create_oval(x - bee_size, y - bee_size, x + bee_size, y + bee_size, fill=bee.color)

    def DrawVisionField(self, bee):
        start_angle = (np.degrees(bee.orientation) - bee.vision_angle / 2) % 360
        extent = bee.vision_angle
        if start_angle > 0:
            start_angle += extent

        # Create the arc
        self.canvas.create_arc(bee.x - bee.vision_range, bee.y - bee.vision_range, bee.x + bee.vision_range, bee.y + bee.vision_range,
                            start=-start_angle, extent=extent, outline='lightblue', width=1)

    def DrawPath(self, bee):
        if bee.path:
            self.canvas.create_line(bee.path, fill='#ffea61', width=1)
    
    def CheckBoundaryCollision(self, bee): 
        if 0+5 < bee.x < self.size-5 and 0+5 < bee.y < self.size-5:
            return
        bee.orientation += np.pi/3

    def DataSave(self): 
        print(f'Data save at timestep: {self.timestep}')
        self.currentFData.append(self.environment.FlowerDistribution())
        self.currentBData.append(self.swarm.BeeDistribution())

        if self.timestep % self.seasonLength == 0 and self.timestep>0: # Only by season change

            if (len(self.environment.flowers) != 0) and (len(self.swarm.bees) != 0):
                self.fbRatio.append(len(self.environment.flowers)/len(self.swarm.bees))
            else:
                self.fbRatio.append(0)
        
    def RunQuarter(self, quarter):
        """
        Tar över stafettpinnen och kör simulationen en hel quarter, eller tills alla bin är döda
        """

        for _ in range(int(0.25*self.seasonLength)):
            self.timestep += 1
            self.swarm.PushUpdate(self.environment.flowers,self.timestep)
            self.environment.PushUpdate(self.timestep)

            if self.visualize:
                self.visualizationUpdate()

            if len(self.swarm.bees) == 0:
                #print(f'All bees are dead, time: {self.timestep}')
                self.timestep = self.seasonLength*(self.season + 0.25*quarter)
                break

    def RunSimulation(self):
        quarters = [1, 2, 3, 4]
        startTime = time.time()
        SimulationBar = tqdm(total=self.simulationLength*self.seasonLength, desc="Progress simulation:", unit="Time steps")
        for season in range(self.simulationLength):
            seasonStart = time.time()
            # Use tqdm function with an external iterator
            #SimulationBar = tqdm(total=self.simulationLength*self.seasonLength, desc="Progress simulation:", unit="Time steps")
            #SeasonBar = tqdm(total=self.seasonLength, desc=f"Progress, season: {self.season+1}", unit="Time steps")

            # Create new generation
            if season > 0:
                #print('Creating the new generation')
                self.environment.newNests = self.swarm.newNests
                self.environment.CreateNewGeneration(self.timestep)
                self.swarm.CreateNewGeneration(self.timestep, self.environment.nests)

            for quarter in quarters:
                # [0-25%, 25-50%, 50-75%, 75-100%]
                self.DataSave()
                self.RunQuarter(quarter)
                #SeasonBar.update((self.timestep-self.season*self.seasonLength))
                SimulationBar.update(self.timestep)
            #SeasonBar.close()
            #SimulationBar.close()
            self.season += 1

            # Save plotting data
            self.flowerData.append(np.copy(self.currentFData))
            self.beeData.append(np.copy(self.currentBData))
            self.currentFData = []
            self.currentBData = []
            print(f'Time to simulate season {self.season}: {(time.time()-seasonStart)//60:2.0f} minutes and {(time.time()-seasonStart)%60:2.0f} seconds.\n')

        # Plot data
        SimulationBar.close()
        print(f'Simulation time: {(time.time() - startTime)//60:2.0f} minutes and {(time.time()-startTime)%60:2.0f} seconds.')
        self.lifespanData = self.swarm.RIP_ages
        self.eggsData = self.swarm.RIP_number_of_eggs
        self.visitedFlowers = self.swarm.RIP_visitedflowers
        self.bee_types = self.swarm.RIP_types
        self.beeDataHistory = self.swarm.RIP_Generation
        
        #MergePlots(self.flowerData, self.beeData, self.lifespanData, self.eggsData, self.visitedFlowers, self.bee_types, self.beeDataHistory, self.fbRatio)

        return self.flowerData, self.beeData, self.lifespanData, self.eggsData, self.visitedFlowers, self.bee_types, self.beeDataHistory, self.fbRatio
        

class BeeSim():
    def __init__(self, size=1000, num_bees=4, num_flowers=200, envType='countryside', beeDist = 'random', NumSeason=10, seasonLength=1000):
        # Define grid and start simulation
        self.size = size
        self.num_flowers = num_flowers
        self.num_bees = num_bees
        self.seasonLength = seasonLength #112000
        self.envType = envType
        self.timestep = 0
        self.season = 0
        self.simulationLength = NumSeason
        self.beeDist = beeDist

        #for plot
        self.flowersPlot = []
        self.beesPlot = []

        # Plot data
        self.currentFData = []
        self.flowerData = []
        self.currentBData = []
        self.beeData = []
        self.currentLData = []
        self.lifespanData = []
        self.eggsData = []
        self.visitedFlowers = []
        self.beeDataHistory = []
        self.bee_types =[]
        self.fbRatio = [num_flowers/num_bees]

        self.simulationSetup()

    def simulationSetup(self):
        self.environment = Environment(self.size, self.seasonLength, self.envType)
        self.environment.InitializeFlowers(self.num_flowers)
        self.environment.InitializeBeeNest(self.num_bees)
        
        self.swarm = Swarm(self.seasonLength)
        self.swarm.InitializeBees(self.num_bees, self.environment.nests,self.beeDist)

    def simulationUpdate(self):
        pass

   # def runSimulation(self):
        #pass


    def DataSave(self): 
        print(f'Data save at timestep: {self.timestep}')
        self.currentFData.append(self.environment.FlowerDistribution())
        self.currentBData.append(self.swarm.BeeDistribution())

        if self.timestep % self.seasonLength == 0 and self.timestep>0: # Only by season change

            if (len(self.environment.flowers) != 0) and (len(self.swarm.bees) != 0):
                self.fbRatio.append(len(self.environment.flowers)/len(self.swarm.bees))
            else:
                self.fbRatio.append(0)
        
    def RunQuarter(self, quarter):
        """
        Tar över stafettpinnen och kör simulationen en hel quarter, eller tills alla bin är döda
        """

        for _ in range(int(0.25*self.seasonLength)):
            self.timestep += 1
            self.swarm.PushUpdate(self.environment.flowers,self.timestep)
            self.environment.PushUpdate(self.timestep)


            if len(self.swarm.bees) == 0:
                #print(f'All bees are dead, time: {self.timestep}')
                self.timestep = self.seasonLength*(self.season + 0.25*quarter)
                break

    def RunSimulation(self):
        quarters = [1, 2, 3, 4]
        startTime = time.time()
        SimulationBar = tqdm(total=self.simulationLength*self.seasonLength, desc="Progress simulation:", unit="Time steps")
        for season in range(self.simulationLength):
            seasonStart = time.time()
            # Use tqdm function with an external iterator
            #SimulationBar = tqdm(total=self.simulationLength*self.seasonLength, desc="Progress simulation:", unit="Time steps")
            #SeasonBar = tqdm(total=self.seasonLength, desc=f"Progress, season: {self.season+1}", unit="Time steps")


            # Create new generation
            if season > 0:
                #print('Creating the new generation')
                self.environment.newNests = self.swarm.newNests
                self.environment.CreateNewGeneration(self.timestep)
                self.swarm.CreateNewGeneration(self.timestep, self.environment.nests)
                #self.lifespanData = self.swarm.RIP_ages
                #self.eggsData = self.swarm.RIP_number_of_eggs
                #self.visitedFlowers = self.swarm.RIP_visitedflowers
                #self.bee_types = self.swarm.RIP_visitedflowers
                #self.beeDataHistory = self.swarm.RIP_Generation

            for quarter in quarters:
                # [0-25%, 25-50%, 50-75%, 75-100%]
                self.DataSave()
                self.RunQuarter(quarter)
                #SeasonBar.update((self.timestep-self.season*self.seasonLength))
                SimulationBar.update(self.timestep)
            #SeasonBar.close()
            #SimulationBar.close()
            self.season += 1

            # Save plotting data
            self.flowerData.append(np.copy(self.currentFData))
            self.beeData.append(np.copy(self.currentBData))
            self.currentFData = []
            self.currentBData = []
            print(f'Time to simulate season {self.season}: {(time.time()-seasonStart)//60:2.0f} minutes and {(time.time()-seasonStart)%60:2.0f} seconds.\n')

        # Plot data

        self.lifespanData = self.swarm.RIP_ages
        self.eggsData = self.swarm.RIP_number_of_eggs
        self.visitedFlowers = self.swarm.RIP_visitedflowers
        self.bee_types = self.swarm.RIP_types
        self.beeDataHistory = self.swarm.RIP_Generation
        
        SimulationBar.close()
        print(f'Simulation time: {(time.time() - startTime)//60:2.0f} minutes and {(time.time()-startTime)%60:2.0f} seconds.')
        
        #MergePlots(self.flowerData, self.beeData, self.lifespanData, self.eggsData, self.visitedFlowers, self.bee_types, self.beeDataHistory, self.fbRatio)

        return self.flowerData, self.beeData, self.lifespanData, self.eggsData, self.visitedFlowers, self.bee_types, self.beeDataHistory, self.fbRatio
        


