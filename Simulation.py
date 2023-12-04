import tkinter as tk
import numpy as np

from tkinter import Scale

from Bee import *
from Environment import *
import matplotlib.pyplot as plt

class BeeSim(tk.Tk):
    def __init__(self, size=500, num_bees=1, num_flowers=1, envType='countryside'):
        super().__init__()
        self.size = size
        self.num_flowers = num_flowers
        
        self.timestep = 0
        self.season = 1

        self.title("Bee Simulation")
        
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side="left", padx=10)
        self.canvas = tk.Canvas(self.canvas_frame, width=size, height=size, bg='#355E3B')
        self.canvas.pack()

        # Frame for sliders
        self.slider_frame = tk.Frame(self)
        self.slider_frame.pack(side="right", padx=10)

        # Sliders for controlling parameters
        self.angular_noise_slider = Scale(self.slider_frame, label="Angular Noise", from_=0.0, to=1.0, resolution=0.01, orient="horizontal", length=200)
        self.angular_noise_slider.set(0.1)
        self.angular_noise_slider.pack()

        self.vision_range_slider = Scale(self.slider_frame, label="Vision Range", from_=10, to=100, orient="horizontal", length=200)
        self.vision_range_slider.set(30)
        self.vision_range_slider.pack()

        self.vision_angle_slider = Scale(self.slider_frame, label="Vision Angle", from_=0, to=359, resolution=1, orient="horizontal", length=200)
        self.vision_angle_slider.set(280)
        self.vision_angle_slider.pack()

        self.show_vision_var = tk.BooleanVar(value=True)
        self.draw_vision_checkbox = tk.Checkbutton(self.slider_frame, text="Draw Vision", variable=self.show_vision_var, onvalue=True, offvalue=False)
        self.draw_vision_checkbox.pack(pady=5)

        self.environment = Environment(size, envType)
        self.environment.InitializeFlowers(num_flowers)
        self.environment.InitializeBeeNest(num_bees)
        
        #for plot
        self.flowersPlot = []
        self.beesPlot =[]
        #ages_first_bees = np.random.randint(-200, 0, size=num_bees) # random birth-dates on first bees
        #pollen_first_bees = [abs(age) for age in ages_first_bees] # so first bees that are old don't starve immediately
        #NOTE: They should be initialized with the amount of food that is collected for them
        self.swarm = Swarm()
        #Skapa en lista av nests 
        self.swarm.InitializeBees(num_bees, self.environment.nests)
        #Skicka 

        self.after(50, self.UpdateModel) #NOTE: Model updates after 50 milli seconds?
        
    def DrawEnvironment(self):
        
        size = 3
        outer_size = 8
        
        for flower in self.environment.flowers:
            x, y = flower.x, flower.y
            self.canvas.create_oval(x - outer_size, y - outer_size, x + outer_size, y + outer_size, fill=flower.outerColor)
            self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=flower.centerColor)
        
        nest_size = 5
        
        for nest in self.environment.nests:
            x, y = nest.x, nest.y
            self.canvas.create_rectangle(x - nest_size, y - nest_size, x + nest_size, y + nest_size, fill=nest.color)
        
        self.environment.PushUpdate(self.timestep)
        
    def DrawBee(self, bee):
        x, y = bee.x, bee.y
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=bee.color)

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

    def UpdateModel(self):
        self.canvas.delete('all')
        self.timestep += 1

        self.title(f"Bee Simulation - time: {self.timestep} | season: {self.season}")

        angular_noise = float(self.angular_noise_slider.get())
        vision_range = int(self.vision_range_slider.get())
        vision_angle = float(self.vision_angle_slider.get())

        #(self, flowers, time, angular_noise, vision_range, vision_angle):
        self.DrawEnvironment() 

        self.swarm.PushUpdate(self.environment.flowers,self.timestep,angular_noise,vision_range,vision_angle)

        for bee in self.swarm.activeBees:
            #This needs to be sent to push update
            self.CheckBoundaryCollision(bee)
            self.DrawBee(bee)
            self.DrawPath(bee)

            if self.show_vision_var.get():
                self.DrawVisionField(bee)  
        
        #Just nu har alla bin samma angular noise, vision range, vision angle
        if self.timestep % 2000==0:
            self.flowersPlot.append(len(self.environment.flowers))
            self.beesPlot.append(len(self.swarm.bees))
            plt.figure()
            plt.plot(self.flowersPlot,label='flowers',c='pink')
            plt.plot(self.beesPlot,label='bees',c='yellow')
            plt.show()
        """
            newBorn = {}
            newNests = []
            for bee_number, bee in enumerate(self.swarm.bees):
                if len(bee.egg) != 0:
                    newBorn[bee_number] = bee.egg # egg = [[nest],nEggs]
                    for egg in bee.egg:
                        newNests.append(egg[0])

            self.environment.CreateNewGeneration(self.timestep, newNests)
            self.swarm.CreateNewGeneration(newBorn, self.environment.nests, self.timestep)
            print('n.o. bees:',len(self.swarm.bees))
            print('n.o. flowers:',len(self.environment.flowers))
            """
            #Vi vill ha koordninaterna för de nya bina :)
        
        #NOTE: Denna delen borde typ vara i bee.py :/
        if self.timestep % self.environment.seasonLength==0 and self.timestep>0:
            self.season += 1
            newnests = []
            parent_traits = []
            for bee in self.swarm.bees:
                #Lägg till typ!
                if len(bee.egg) != 0:
                    for egg in bee.egg:  
                        self.environment.newNests.append(egg)
                        parent_traits.append(bee.Beetraits)

            self.environment.CreateNewGeneration(self.timestep)
            self.swarm.CreateNewGeneration(self.environment.nests,parent_traits, 0)

            
        self.after(50, self.UpdateModel)

    
if __name__ == "__main__":
    bee_sim = BeeSim(size=600, num_bees=9, num_flowers=150, envType='countryside')
    bee_sim.mainloop()

