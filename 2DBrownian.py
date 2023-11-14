import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
#import imageio  
import numpy as np

class Bee:
    def __init__(self, x, y, size=0.02, color=(0.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.size = size
        self.path = [[self.x,self.y]]
        self.velocity = [0.01,0.01]
        self.color = color
        self.fed = 0         # 0=hungry, 1 = fed?
        self.max_speed = 0.05

    def update(self, environment):
        
        
        #currentPosition = (self.x,self.y)
        #lastPosition = self.path[-1]
        #self.velocity = np.array(currentPosition) - np.array(lastPosition)
        
        speed = np.linalg.norm(self.velocity)
        delta_speed = np.random.randint(-5,10)/10**5
        new_speed = speed + delta_speed
        if new_speed > self.max_speed:
            new_speed = self.max_speed
        
        if abs(self.x) >= 1:
            self.velocity = [-self.velocity[0]*1.5,self.velocity[1]]
        if abs(self.y) >= 1:
            self.velocity = [self.velocity[0],-self.velocity[1]*1.5]
        
        
        angle_change_rate = 5/10**4
        delta_velocity = np.array([np.random.randint(-10,10)*angle_change_rate, np.random.randint(-10,10)*angle_change_rate])
        new_velocity = np.array(self.velocity + delta_velocity)
        norm = np.linalg.norm(new_velocity)
        if norm == 0:
            norm = 0.0001
        self.velocity = (new_velocity/norm) * new_speed
        
        

        delta_x = self.velocity[0]
        delta_y = self.velocity[1]
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        
        self.path.append((self.x, self.y))
        
        
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


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    environment = []
    particle = Bee(0, 0,color=(1,1,0))
    
    # writer = imageio.get_writer('brownian_motion_with_trace.gif', duration=0.1)

    #while True:
    for i in range(500):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if i == 499:
            pygame.quit()
            quit()
            break

        
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.2, 0.2, 0.2, 0.2)
        
        particle.update(environment)
        particle.draw()
        particle.draw_path()

        # Capture the current frame
        data = glReadPixels(0, 0, *display, GL_RGB, GL_UNSIGNED_BYTE)
        image = pygame.image.fromstring(data, display, 'RGB')
        frame = pygame.surfarray.array3d(image)

        # Flip the frame vertically
        frame = np.flipud(frame)

  
        # writer.append_data(frame)

        pygame.display.flip()
        pygame.time.wait(100)


    # writer.close()

if __name__ == "__main__":
    main()
