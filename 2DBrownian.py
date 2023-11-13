import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
#import imageio  
import numpy as np

class Bee:
    def __init__(self, x, y, stepLength = 0.01, size=0.02, color=(0.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.size = size
        self.path = []
        self.color = color
        self.fed = 0         # 0=hungry, 1 = fed?
        self.stepLength = stepLength

    def update(self, environment):
        delta_x = np.random.normal(0, self.stepLength)
        delta_y = np.random.normal(0, self.stepLength)
        
       
        self.x = (self.x + delta_x)
        self.y = (self.y + delta_y)

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
    particle = Bee(0.5, 0.5,color=(1,1,0))
    
    # writer = imageio.get_writer('brownian_motion_with_trace.gif', duration=0.1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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
        pygame.time.wait(10)

    # writer.close()

if __name__ == "__main__":
    main()
