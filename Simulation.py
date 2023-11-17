import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

from Bee import * 
from Environment import *


def draw_environment(env):
        size = 10
        color = (1.0, 1.0, 1.0)
        glColor3f(*color)
        for flower in env.flowers:

            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(flower.x, flower.y)
            num_segments = 100
            for i in range(num_segments + 1):
                theta = (2.0 * np.pi * i) / num_segments
                x = flower.x + size * np.cos(theta)
                y = flower.y + size * np.sin(theta)
                glVertex2f(x, y)
            glEnd()


def main():
    
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    nearby = [[0.001,'right',0.5,0.5],[0.003,'left',-0.5,-0.5]] 
    
    environment = Environment([800, 600])
    environment.InitializeFlowers()

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
        

        draw_environment(environment)

        particle.update()
        particle.draw()
        particle.draw_path()
        particle.draw_vision_field()
        found_flower, empty_flower = particle.find_flowers(nearby)
        if found_flower:
            nearby.pop(nearby.index(empty_flower))  # should not be nearby

        
        # Capture the current frame
        data = glReadPixels(0, 0, *display, GL_RGB, GL_UNSIGNED_BYTE)
        image = pygame.image.fromstring(data, display, 'RGB')
        frame = pygame.surfarray.array3d(image)

        # Flip the frame vertically
        frame = np.flipud(frame)

  
        # writer.append_data(frame)

        pygame.display.flip()
        pygame.time.wait(50)
        

    # writer.close()


def main_no_game():    # For testing without plotting

    particle = Bee(0, 0,color=(1,1,0))
    nearby = [[0.001,'right',0.5,0.5],[0.003,'left',-0.5,-0.5]]

    for i in range(500):

        if i == 499:
            break
        particle.update()
        #particle.draw_vision_field()
        found_flower, empty_flower = particle.find_flowers(nearby)
        if found_flower:
            nearby.pop(nearby.index(empty_flower)) # should not be nearby

if __name__ == "__main__":
    main()