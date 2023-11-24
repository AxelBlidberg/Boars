import tkinter as tk
import numpy as np

from tkinter import Scale

from Bee import *
from Environment import *

class BeeSim(tk.Tk):
    def __init__(self, size=500, num_bees=1, num_flowers=1):
        super().__init__()
        self.size = size
        self.num_flowers = num_flowers
        
        self.timestep = 0

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
        self.angular_noise_slider.set(0.45)
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

        self.environment = Environment(size)
        self.environment.InitializeFlowers(num_flowers,self.timestep)
        self.environment.InitializeBeeNest(num_bees)
        

        ages_first_bees = np.random.randint(-200, 0, size=num_bees) # random birth-dates on first bees
        pollen_first_bees = [abs(age) for age in ages_first_bees] # so first bees that are old don't starve immediately
        self.bees = [Bee(self.environment.nests[i], ages_first_bees[i],{1:pollen_first_bees[i]}) for i in range(num_bees)]

        self.after(50, self.UpdateModel)

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
    
    def CheckBoundaryCollision(self, bee): # fastnar på blommor utanför canvas fixas nog bäst i Environment
        if 0+5 < bee.x < self.size-5 and 0+5 < bee.y < self.size-5:
            return
        bee.orientation += np.pi/2

    def UpdateModel(self):
        self.canvas.delete('all')
        self.timestep += 1

        angular_noise = float(self.angular_noise_slider.get())
        vision_range = int(self.vision_range_slider.get())
        vision_angle = float(self.vision_angle_slider.get())
        
        self.DrawEnvironment() 

        # new bees
        if self.timestep % 50==0: # change to pollen-related
            nest = self.environment.nests[np.random.randint(len(self.environment.nests))] # born in random nest
            self.bees.append(Bee(nest, self.timestep))
        
        for bee_number, bee in enumerate(self.bees):
            
            bee.angular_noise, bee.vision_range, bee.vision_angle = angular_noise, vision_range, vision_angle

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
        
        if self.timestep%200 == 1: # temporary: add 10 flowers every 100th timestep
            self.environment.InitializeFlowers(20, self.timestep)
      
        self.after(50, self.UpdateModel)


    
if __name__ == "__main__":
    bee_sim = BeeSim(size=600, num_bees=5, num_flowers=150)
    bee_sim.mainloop()
