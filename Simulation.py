import tkinter as tk
import numpy as np


from tkinter import Scale
from Bee import *
from Environment import *

class BeeSim:
    def __init__(self, size=500, num_bees=1, num_flowers=1):
        self.size = size
        self.num_flowers = num_flowers

        self.root = tk.Tk()
        self.root.title("Bee Simulation")
        
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side="left", padx=10)
        self.canvas = tk.Canvas(self.canvas_frame, width=size, height=size, bg='#333333')
        self.canvas.pack()

        # Frame for sliders
        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.pack(side="right", padx=10)

        # Sliders for controlling parameters
        self.angular_noise_slider = Scale(self.slider_frame, label="Angular Noise", from_=0.0, to=1.0, resolution=0.01, orient="horizontal", length=200)
        self.angular_noise_slider.set(0.65)
        self.angular_noise_slider.pack()

        self.vision_range_slider = Scale(self.slider_frame, label="Vision Range", from_=10, to=100, orient="horizontal", length=200)
        self.vision_range_slider.set(50)
        self.vision_range_slider.pack()

        self.vision_angle_slider = Scale(self.slider_frame, label="Vision Angle", from_=0, to=360, resolution=1, orient="horizontal", length=200)
        self.vision_angle_slider.set(180)
        self.vision_angle_slider.pack()


        

        self.nearby = [[0.001, 'right', 0.5, 0.5], [0.003, 'left', -0.5, -0.5]]

        self.environment = Environment(size)
        self.environment.InitializeFlowers(num_flowers)

        self.bees = [Bee(np.random.uniform(0, size), np.random.uniform(0, size)) for _ in range(num_bees)]

    def draw_environment(self):
        size = 4
        for flower in self.environment.flowers:
            x, y = flower.x, flower.y
            self.canvas.create_oval(x - size, y - size, x + size, y + size, fill='white')

    def draw_bees(self):
        for bee in self.bees:
            x, y = bee.x, bee.y
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='yellow')

    def draw_vision_field(self):
        for bee in self.bees:
            x, y = bee.x, bee.y
            vision_points = bee.vision_points

            self.canvas.create_line(x, y, vision_points[0][0], vision_points[0][1], fill='blue', width=2)
            self.canvas.create_line(x, y, vision_points[1][0], vision_points[1][1], fill='blue', width=2)

    def draw_paths(self):
        for bee in self.bees:
            path = bee.path
            if path:
                self.canvas.create_line(path, fill='yellow', width=2)

    def update_model(self):
       
        angular_noise = float(self.angular_noise_slider.get())
        vision_range = int(self.vision_range_slider.get())
        vision_angle = (float(self.vision_angle_slider.get())*2*np.pi)/360

        for bee in self.bees:
            bee.angular_noise, bee.vision_range, bee.vision_angle = angular_noise, vision_range, vision_angle
            bee.update(self.environment.flowers)
            self.check_boundary_collision(bee)

        self.canvas.delete('all')

        self.draw_environment()
        self.draw_bees()

        for bee in self.bees:
            found_flower, empty_flower = bee.find_flowers(self.nearby)
            if found_flower:
                self.nearby.pop(self.nearby.index(empty_flower))

        #self.draw_vision_field()
        self.draw_paths()

        self.root.after(50, self.update_model)
    
    def check_boundary_collision(self, bee):

        if bee.x < 0+5 or bee.x > self.size-5:
            bee.velocity[0] *= -1
        if bee.y < 0+5 or bee.y > self.size-5:
            bee.velocity[1] *= -1 
    
    def run_simulation(self):
        self.root.after(0, self.update_model)
        self.root.mainloop()

if __name__ == "__main__":
    bee_sim = BeeSim(size= 800, num_bees=4, num_flowers=200)
    bee_sim.run_simulation()
