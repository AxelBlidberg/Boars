import numpy as np
import turtle
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, size) -> None:
        self.xLimit = size
        self.yLimit = size
        self.flowers = []
        self.hazards = []

    def GetSurroundings(self, position, radius):
        '''
        Returns list sorted on distance on the format: [distance, type, x, y], ex: [1, flower: rose, x, y]

        position = position of the bee
        radius = How far away to check
        '''
        Euclidan = lambda x1, x2: np.sqrt(sum([(x1[i] - x2[i])**2 for i in range(len(x1))]))
        nearby = []
        for i in range(len(self.flowers)):
            x = self.flowers[i].x
            y = self.flowers[i].y
            distance = Euclidan(position, [x, y])
            if distance <= radius:
                nearby.append([distance, 'flower', x, y])

        nearby = sorted(nearby, key= lambda x: x[0])
        return nearby

    def AddFlower(self, n):
        '''
        Method to add one or several flowers to the environment

        n = Number of flowers to add
        size = Size of the environment for correct placement of flowers
        '''
        for _ in range(n):
            x = self.xLimit*np.random.rand()
            y = self.yLimit*np.random.rand()
            temp = Flower(x,y)
            self.flowers.append(temp)

    def AddBeeNest(self):
        pass

    def ExportContent(self):
        '''
        Exports a list of the format [class, 'Type', x, y] ex: ['flower', 1, x, y]
        '''
        content = []

        for flower in self.flowers:
            content.append(['flower', flower.type, flower.x, flower.y])
        
        return content

class Flower:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.type = np.random.randint(1, 5)
        self.nectarAmount = np.random.randint(1,10)

        self.pollen = 0
        

    
    def decreaseNectar(self):
        self.nectarAmount -= 1

    #add Pollen 

class Hazards(Environment):
    def __init__(self, size) -> None:
        super().__init__(size)



test = Environment(10)

test.AddFlower(5)
print(len(test.flowers))
neighbors = test.GetSurroundings([5,5], 5)
A = test.ExportContent()
print(neighbors)
print(A)

