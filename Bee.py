import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

class Bee:
    def __init__(self, x, y, size=0.02, color=(0.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.size = size
        self.path = [[self.x,self.y]]
        self.velocity = [0.01,0.01]
        self.color = color
        self.nectar = 0         # 0=hungry, 1 = fed?
        self.pollen = {}        # how much pollen and what kind
        self.max_speed = 0.05
        self.vision_length = 0.2
        # add self.speed? (= norm of velocity)

    def update(self):
        minimum_norm = 0.0001
        speed_change_rate = 1/10**5
        angle_change_rate = 5/10**4
        
        speed = np.linalg.norm(self.velocity)
        delta_speed = np.random.randint(-5,5)*speed_change_rate
        new_speed = speed + delta_speed
        if new_speed > self.max_speed:
            new_speed = self.max_speed
        
        # Bounce on walls
        if abs(self.x) >= 1:
            self.velocity = [-self.velocity[0]*1.5,self.velocity[1]]
        if abs(self.y) >= 1:
            self.velocity = [self.velocity[0],-self.velocity[1]*1.5]
        
        delta_velocity = np.array([np.random.randint(-10,10)*angle_change_rate, np.random.randint(-10,10)*angle_change_rate])
        new_velocity = np.array(self.velocity + delta_velocity)
        norm = np.linalg.norm(new_velocity)
        if norm == 0: # can be 0 if speed = 0? Remove this possibility?
            norm = minimum_norm
        self.velocity = (new_velocity/norm) * new_speed
        
        delta_x = self.velocity[0]
        delta_y = self.velocity[1]
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        self.path.append((self.x, self.y))
        
    def choose_flower(self, nearby):  
        # assuming "radius" in environment = "vision length" here
        empty_flower = []
        found_flower = False

        nearest_flower = [1000]
        
        for flower in nearby:
            if flower[0] < nearest_flower[0]:  #[0] --> distance
                nearest_flower = flower
                found_flower = True

        if found_flower: 
            # go to coordinates of flower
            self.x,self.y = nearest_flower[2],nearest_flower[3]
            print('found flower',nearest_flower)
            empty_flower = nearest_flower
        
        return found_flower, empty_flower
        
    def draw(self):

        glColor3f(*self.color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(self.x, self.y)
        num_segments = 100
        for i in range(num_segments + 1):
            theta = (2.0 * np.pi * i) / num_segments
            x = self.x + self.size * np.cos(theta)
            y = self.y + self.size * np.sin(theta)
            glVertex2f(x, y)
        glEnd()

    def draw_path(self):
        glColor3f(*self.color)
        glLineWidth(2.0)
        glBegin(GL_LINE_STRIP)
        for pos in self.path:
            glVertex2f(pos[0], pos[1])
        glEnd()
