import tkinter as tk
import numpy as np

from tkinter import Scale

from Bee import *
from Environment import *
from Result import *
import matplotlib.pyplot as plt

class BeeSim(tk.Tk):
    def __init__(self, size=112000, num_bees=4, num_flowers=200, envType='countryside',visualize=False, runTime=10):
        super().__init__()
        # Define grid and start simulation
        self.size = size
        self.num_flowers = num_flowers
        self.seasonLength = 1000 #112000
        self.timestep = 0
        self.season = 0
        self.visualize = visualize
        self.simulationLength = runTime

        if self.visualize:
            self.title("Bee Simulation")
        
            self.canvas_frame = tk.Frame(self)
            self.canvas_frame.pack(side="left", padx=10)
            self.canvas = tk.Canvas(self.canvas_frame, width=size, height=size, bg='#355E3B')
            self.canvas.pack()

            # Frame for sliders
            self.slider_frame = tk.Frame(self)
            self.slider_frame.pack(side="right", padx=10)

            self.show_vision_var = tk.BooleanVar(value=True)
            self.draw_vision_checkbox = tk.Checkbutton(self.slider_frame, text="Draw Vision", variable=self.show_vision_var, onvalue=True, offvalue=False)
            self.draw_vision_checkbox.pack(pady=5)

        self.environment = Environment(size, self.seasonLength, envType)
        self.environment.InitializeFlowers(num_flowers)
        self.environment.InitializeBeeNest(num_bees)
        
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
        self.flowerBeeRatio = [num_flowers/num_bees]

        self.swarm = Swarm(self.seasonLength)
        self.swarm.InitializeBees(num_bees, self.environment.nests)

    def DrawEnvironment(self):
        
        flower_size = 3
        
        for flower in self.environment.flowers:
            x, y = flower.x, flower.y
            self.canvas.create_oval(x - flower_size, y - flower_size, x + flower_size, y + flower_size, fill=flower.color)
        
        nest_size = 3
        
        for nest in self.environment.nests:
            x, y = nest.x, nest.y
            self.canvas.create_rectangle(x - nest_size, y - nest_size, x + nest_size, y + nest_size, fill=nest.color)
        
        self.environment.PushUpdate(self.timestep)
        
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
        print(f'\nData save at timestep: {self.timestep}')
        self.currentFData.append(self.environment.FlowerDistribution())
        self.currentBData.append(self.swarm.BeeDistribution(0))

        if self.timestep % self.seasonLength == 0 and self.timestep>0: # Only by season change
            
            self.lifespanData = self.swarm.RIP_ages
            self.eggsData = self.swarm.RIP_number_of_eggs
            self.visitedFlowers = self.swarm.RIP_visitedflowers
            self.bee_types = self.swarm.RIP_visitedflowers
            if (len(self.swarm.bees) != 0) and (len(self.environment.flowers) != 0):
                self.flowerBeeRatio.append(len(self.environment.flowers)/len(self.swarm.bees))
            else:
                self.flowerBeeRatio.append(0)  

    def RunQuarter(self, quarter):
        """
        Tar över stafettpinnen och kör simulationen en hel quarter, eller tills alla bin är döda
        """
        print('Q:',quarter)
        print('n.o. bees:', len(self.swarm.activeBees))
        print('n.o. flowers:',len(self.environment.flowers))
        for step in range(int(0.25*self.seasonLength)):
            self.timestep += 1
            self.swarm.PushUpdate(self.environment.flowers,self.timestep)
            self.environment.PushUpdate(self.timestep)

            if self.visualize:
                self.canvas.delete('all')
                self.title(f"Bee Simulation - time: {self.timestep} | season: {self.season}")
                self.DrawEnvironment()
                for bee in self.swarm.activeBees:
                    self.CheckBoundaryCollision(bee)
                    self.DrawBee(bee)
                    self.DrawPath(bee)
                    if self.show_vision_var.get():
                        self.DrawVisionField(bee)
            if len(self.swarm.bees) == 0:
                print(f'All bees are dead, time: {self.timestep}')
                #print('season:',self.season, 'quarter:',quarter, 's-length:',self.seasonLength)
                self.timestep = self.seasonLength*(self.season + 0.25*quarter)
                #print(f'When bees are dead, next timestep: {self.timestep}')
                break

    def RunSimulation(self):
        quarters = [1, 2, 3, 4]
        for season in range(self.simulationLength):
            # Create new generation
            if season > 0:
                print('Creating the new generation')
                self.environment.newNests = self.swarm.newNests
                self.environment.CreateNewGeneration(self.timestep)
                self.swarm.CreateNewGeneration(self.timestep, self.environment.nests)
                self.lifespanData = self.swarm.RIP_ages
                self.eggsData = self.swarm.RIP_number_of_eggs
                self.visitedFlowers = self.swarm.RIP_visitedflowers
                self.bee_types = self.swarm.RIP_visitedflowers

            for quarter in quarters:
                # [0-25%, 25-50%, 50-75%, 75-100%]
                self.DataSave()
                self.RunQuarter(quarter)
            
            self.season += 1

            # Save plotting data
            self.flowerData.append(np.copy(self.currentFData))
            self.beeData.append(np.copy(self.currentBData))
            self.currentFData = []
            self.currentBData = []
        
        # Plot data
        MergePlots(self.flowerData, self.beeData, self.lifespanData, self.eggsData, self.visitedFlowers, self.bee_types, self.beeData, self.flowerBeeRatio)


