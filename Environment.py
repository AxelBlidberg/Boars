import numpy as np
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, size) -> None:
        self.xLimit = size
        self.yLimit = size
        self.flowers = []
        self.nests = []
        self.hazards = []
        self.iterations = 1

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

    def InitializeFlowers(self, n):
        '''
        Initializes n number of flowers in the environment
        '''
        for _ in range(n):
            center = [self.xLimit/2, self.yLimit/2]
            self.flowers.append(Flower(center, self.xLimit/2, self.iterations, self.xLimit, self.yLimit))

    def AddFlower(self, center, radius, flowerType):
        '''
        Method to add one or several flowers to the environment

        n = Number of flowers to add
        '''
        self.flowers.append(Flower(center, radius, self.iterations, self.xLimit, self.yLimit, flowerType))

    def InitializeBeeNest(self, n):
        '''
        Method to initialize n nests in the beginning of the simulation
        
        n = Number of nests to add
        '''
        center = [self.xLimit/2, self.yLimit/2]
        for _ in range(n):
            self.nests.append(Nest(center, self.xLimit/2, self.xLimit, self.yLimit))

    def AddBeeNest(self, n):
        '''
        Method to add one or several nests to the environment during the simulation

        n = Number of nests to add
        '''
        pass

    def ExportContent(self):
        '''
        Exports a list of the format [class, 'Type', x, y, object] ex: ['flower', 1, x, y, Flower]
        '''
        content = []

        for flower in self.flowers:
            content.append(['flower', flower.type, flower.x, flower.y, flower])

        for nest in self.nests:
            content.append(['Nest', 'Nest', nest.x, nest.y, nest])
        
        return content

    def PushUpdate(self):
        self.iterations += 1
        # Update flowers
        for i, flower in enumerate(self.flowers):
            status = flower.UpdateFlower(self.iterations)
            if status[0] == 1:
                self.AddFlower(status[1], 2)
            elif status[0] == 2:
                del self.flowers[i]

    def GetObject(self, x, y):
        '''
        Returns the object at the specified location for outside manipulation of object, like depositing/ taking pollen.

        x = X coordinate
        y = Y coordinate
        type = Which type of object
        '''
        content = self.ExportContent()
        for i in range(len(content)):
            if content[i][2] == x and content[i][3] == y:
                return content[i][-1]


class Flower:
    def __init__(self, center, radius, birth, xLimit, yLimit, t='random') -> None:
        # Add control to ensure location is within environment
        self.x = center[0] + radius*np.random.uniform(-1, 1)
        if self.x < 0:
            self.x = 0
        elif self.x > xLimit:
            self.x = xLimit
        self.y = center[1] + radius*np.random.uniform(-1, 1)
        if self.y < 0:
            self.y = 0
        elif self.y > yLimit:
            self.y = yLimit
        self.location = [self.x, self.y]
        if t == 'random':
            self.type = np.random.randint(1, 5)
        else:
            self.type = t
        self.flowersize = np.random.randint(1, 5)
        self.nectarAmount = np.random.randint(1,10)
        self.pollen = {f'{i}': 0 for i in range(1,6)}
        self.lifespan = 100
        self.creation = birth

    def __str__(self) -> str:
        return f'Flower of type: {self.type} at ({self.x:3.1f}, {self.y:3.1f})'

    def DecreaseNectar(self):
        '''
        Decreases the nectar in a flower
        '''
        if self.nectarAmount < 0:
            self.nectarAmount -= 1
    
    def Pollination(self, beeInstance):
        '''
        Pollinates flowers depending on the pollen carried by a bee
        '''
        for pollenType, amount in beeInstance.pollenCarried.items():
            self.pollen[pollenType] += amount

    def UpdateFlower(self, time):
        '''
        Update rules for flowers, 
        '''
        if self.pollen[f'{self.type}'] >= 10:
            self.pollen[self.type] -= 10
            return [1, [self.x, self.y]]
        elif time - self.creation < self.lifespan:
            return [2, []]
        else:
            return [0, []]


class Nest:
    def __init__(self, center, radius, xLimit, yLimit) -> None:

        # Location of the nest
        self.x = center[0] + radius*np.random.uniform(-1, 1)
        if self.x < 0:
            self.x = 0
        elif self.x > xLimit:
            self.x = xLimit
        self.y = center[1] + radius*np.random.uniform(-1, 1)
        if self.y < 0:
            self.y = 0
        elif self.y > yLimit:
            self.y = yLimit
        self.location = [self.x, self.y]
    

    def GetLocation(self) -> list:
        '''
        Returns the coordinates of a nest
        '''
        return [self.x, self.y]
    
    def __str__(self) -> str:
        return f'Nest at ({self.x}, {self.y})'

    def IsOccupied(self, nestInstance) -> bool:
        '''
        Checks if a nest is occupied by a bee
        '''
        pass

    def AssignNest(self, nestInstance, beeInstance):
        '''
        Assign a nest to a bee
        '''
        if not self.IsOccupied(nestInstance):
            pass        


class Hazards:
    def __init__(self) -> None:
        pass


def PlotFunction(data, limit):
    '''
    Temporary function for plotting the environment. Takes a special formatted list obtained from the ExportContent method in the Environment class.
    '''
    # Divide data
    flowers = []
    for object in data:
        if object[0] == 'flower':
            flowers.append(object)

    nests = []
    for object in data:
        if object[0] == 'Nest':
            nests.append(object)

    types = [item[1] for item in flowers]
    x_values = [item[2] for item in flowers]
    x_NestValues = [item[2] for item in nests]
    y_values = [item[3] for item in flowers]
    y_NestValues = [item[3] for item in nests]

    unique_types = set(types)
    color_map = {t: i for i, t in enumerate(unique_types)}
    colors = [color_map[t] for t in types]

    plt.scatter(x_values, y_values, c=colors, cmap='viridis', s=50, alpha=0.8, label=types)
    plt.scatter(x_NestValues, y_NestValues, marker='^', color='black', label='Black Triangles', s=100)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot with Colors')
    plt.xlim([0, limit])
    plt.ylim([0, limit])
    plt.show()



test = Environment(100)

test.InitializeFlowers(5)

test.InitializeBeeNest(5)

for i in range(10):
    obj = np.random.choice(test.flowers)
    test.AddFlower(obj.location, 5, obj.type)

for i in range(10):
    obj = np.random.choice(test.flowers)
    C = test.GetObject(obj.x, obj.y)
    print(f'Selected flower: {C}')




#neighbors = test.GetSurroundings([5,5], 5)
A = test.ExportContent()
B = test.flowers
#for b in B:
#    print(b)

for a in A:
    print(a)
test.PushUpdate()

PlotFunction(A, 100)

