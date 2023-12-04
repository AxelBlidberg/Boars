import tkinter as tk
import numpy as np

from tkinter import Scale

from Bee import *
from Environment import *

from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class BeeSim(tk.Tk):
    def __init__(self, size=500, num_bees=1, num_flowers=1, envType='countryside'):
        super().__init__()
        self.size = size
        self.num_flowers = num_flowers
        
        self.timestep = 0

        self.title("Bee Simulation")
        
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side="left", padx=10)
        self.canvas = tk.Canvas(self.canvas_frame, width=size, height=size, bg='#355E3B')
        self.canvas.pack()

        # Plotting 
        self.plot_canvas_frame = tk.Frame(self)
        self.plot_canvas_frame.pack(padx=10)
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, self.plot_canvas_frame)
        self.plot_canvas.get_tk_widget().pack()
        self.figure.suptitle('Population count')
        self.figure.legend()
        self.axes = self.figure.subplot_mosaic(
            """
            AAA
            BBB
            """
        )
        self.ani = None
        self.bee_population_count = []
        self.flower_population_count = []
        
        
        # Frame for sliders
        self.slider_frame = tk.Frame(self)
        self.slider_frame.pack(padx=10)

        self.show_vision_var = tk.BooleanVar(value=False)
        self.draw_vision_checkbox = tk.Checkbutton(self.slider_frame, text="Draw Vision", variable=self.show_vision_var, onvalue=True, offvalue=False)
        self.draw_vision_checkbox.pack(pady=5)

        self.environment = Environment(size, envType)
        self.environment.InitializeFlowers(num_flowers)
        self.environment.InitializeBeeNest(num_bees)
        
        ages_first_bees = np.random.randint(-200, 0, size=num_bees) # random birth-dates on first bees
        pollen_first_bees = [abs(age) for age in ages_first_bees] # so first bees that are old don't starve immediately
        #NOTE: They should be initialized with the amount of food that is collected for them
        self.bees = [Bee(self.environment.nests[i], ages_first_bees[i],{1:pollen_first_bees[i]}) for i in range(num_bees)]


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
        bee.orientation += np.pi/2

    def UpdateModel(self, frame):
        self.canvas.delete('all')
        self.timestep += 1
        
        self.DrawEnvironment() 
        wealth = []
        # new bees
        if self.timestep % 50==0: # change to pollen-related
            nest = self.environment.nests[np.random.randint(len(self.environment.nests))] # born in random nest
            self.bees.append(Bee(nest, self.timestep))
        
        for bee_number, bee in enumerate(self.bees):
            
        
            # kill bee if old
            bee_age = self.timestep - bee.birth
            if  bee_age > bee.max_age: 
                print('RIP: bee died of age:',bee_age,'. Pollen levels:',bee.pollen)
                self.bees.pop(bee_number)
                del bee
                continue
            
            # kill bee if starving
            food = sum(bee.pollen.values())
            if food < 1 and bee_age > 100:
                print('RIP: bee died of starvation. Age:',bee_age,'. Pollen levels:',bee.pollen)
                self.bees.pop(bee_number)
                del bee
                continue
            full = 500
            if food > full:
                bee.ReturnHome() # return to home nest if full
            else:
                bee.Update(self.environment.flowers)
            
            
            self.CheckBoundaryCollision(bee)
            self.DrawBee(bee)
            self.DrawPath(bee)

            if self.show_vision_var.get():
                self.DrawVisionField(bee)  
            wealth.append(sum(bee.pollen.values()))

        self.bee_population_count.append(len(self.bees))
        self.flower_population_count.append(len(self.environment.flowers))

        self.axes['A'].clear()
        self.axes['B'].clear()

        self.axes['A'].plot(self.bee_population_count, label='Bees')
        self.axes['A'].plot(self.flower_population_count, label='Flowers')
        self.axes['A'].legend()

        self.axes['B'].hist(wealth)
        self.axes['B'].set_label('Wealth distribution')

    
if __name__ == "__main__":
    bee_sim = BeeSim(size=600, num_bees=5, num_flowers=150, envType='urban')
    bee_sim.ani =  animation.FuncAnimation(bee_sim.figure, bee_sim.UpdateModel, interval=1)
    bee_sim.mainloop()
