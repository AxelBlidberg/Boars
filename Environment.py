import numpy as np
import turtle
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, size) -> None:
        self.xLimit = size
        self.yLimit = size
        self.flowers = []
        self.hazards = []
        self.SuperGrid = [] # Added for faster search around location

    def CreateGrid():
        grid = [[[] for _ in range(10)] for i in range(10)]
        return grid

    def AddFlower(self, n, size):
        '''
        Meth
 eht ot srewolf sdda d
        n = Number of flowers to add
        
        '''
        for i in range(n):
            x = size*np.random.rand()
            y = size*np.random.rand()
            self.append(Flower(x, y))

    def AddBeeNest(self):
        pass

class Flower(Environment):
    def __init__(self, size, x, y) -> None:
        super().__init__(size)

        self.x = x
        self.y = y
        self.size = size
        
        self.nectarAmount = np.random.randint(1,10)

        self.pollen = 0
        

    
    def decreaseNectar(self):
        self.nectarAmount -= 1

    #add Pollen 

class Hazards(Environment):
    def __init__(self, size) -> None:
        super().__init__(size)




#Enkelt bi som rör sig slumpmässigt
'''
class Bee:
    def __init__(self):
        self.bee = turtle.Turtle()
        self.bee.shape('triangle')
        self.bee.color('yellow')
        self.bee.penup()
        self.bee.speed(1)
    
    def moveRight(self):
        self.bee.setheading(0)
        self.bee.forward(10)
    
    def moveUp(self):
        self.bee.setheading(90)
        self.bee.forward(10)

    def moveLeft(self):
        self.bee.setheading(180)
        self.bee.forward(10)
    
    def moveDown(self):
        self.bee.setheading(270)
        self.bee.forward(10)

    
    def randomMove(self):
        direction = np.random.choice(['right', 'up', 'left', 'down'])

        if direction == 'right':
            self.moveRight()
        elif direction == 'up':
            self.moveUp()
        elif direction == 'left':
            self.moveLeft()
        elif direction == 'down':
            self.moveDown()
      

#bee = Bee()

while True:
    bee.randomMove()
    turtle.update()
'''


env = Environment()

env.createGrid()





env.AddFlower(1, 1)


plt.plot(env.)



