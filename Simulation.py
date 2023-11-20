import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from Bee import * 
from Environment import *



def main():
    
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    environment = Environment(1)
    environment.InitializeFlowers(10)
    #nearby = [[0.001,'right',0.5,0.5],[0.003,'left',-0.5,-0.5]] 

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

        flowers = environment.ExportContent()
        nearby = environment.GetSurroundings([particle.x,particle.y], particle.vision_length)

        particle.update()
        particle.draw()
        particle.draw_path()
        found_flower, empty_flower = particle.choose_flower(nearby)
        if found_flower:
            print(flowers)
            flowers.pop(flowers.index(empty_flower))  # should not be nearby
            
        
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
        found_flower, empty_flower = particle.find_flowers(nearby)
        if found_flower:
            nearby.pop(nearby.index(empty_flower)) # should not be nearby

if __name__ == "__main__":
    main()