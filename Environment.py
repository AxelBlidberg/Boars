import numpy as np


class Environment:
    def __init__(self, size, environmentType='countryside') -> None:
        print(f'\nAn environment has been created of type: \'{environmentType}\'')
        self.xLimit = size
        self.yLimit = size
        self.envType = environmentType
        self.flowers = []
        self.nests = []
        self.hazards = []
        self.iterations = 0

    def GetSurroundings(self, position, radius) -> list:
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

    def InitializeFlowers(self, n) -> None:
        '''
        Initializes n number of flowers in the environment
        '''
        for _ in range(n):
            center = [self.xLimit/2, self.yLimit/2]
            self.flowers.append(Flower(center, self.xLimit/2, self.iterations, t='random', environment=self.envType))

    def AddFlower(self, center, radius, flowerType) -> None:
        '''
        Method to add one or several flowers to the environment

        center = Around which coordinate the flower should be created
        radius = distance from center allowed
        flowerType = Which flower should be created
        '''
        self.flowers.append(Flower(center, radius, self.iterations, t=flowerType))

    def InitializeBeeNest(self, n) -> None:
        '''
        Method to initialize n nests in the beginning of the simulation
        
        n = Number of nests to add
        '''
        center = [self.xLimit/2, self.yLimit/2]
        
        for _ in range(n):
            self.nests.append(Nest(center, self.xLimit/2))

    def AddBeeNest(self, center, radius) -> None:
        '''
        Method to add one or several nests to the environment during the simulation

        center = Around which coordinate the nest should be created
        radius = Allowed distance from center
        '''
        self.nests.append(Nest(center, radius))

    def ExportContent(self) -> list:
        '''
        Exports a list of the format [class, 'Type', x, y, object] ex: ['flower', 1, x, y, Flower]
        '''
        content = []

        for flower in self.flowers:
            content.append(['flower', flower.type, flower.x, flower.y, flower])

        for nest in self.nests:
            content.append(['Nest', 'Nest', nest.x, nest.y, nest])
        
        return content

    def FlowerDistribution(self) -> dict:
        distribution = {'Lavender': 0, 'Bee balm': 0, 'Sunflower': 0, 'Coneflower': 0, 'Blueberry': 0}
        for flower in self.flowers:
            if flower.type == 1:
                distribution['Lavender'] += 1
            elif flower.type == 2:
                distribution['Bee balm'] += 1
            elif flower.type == 3:
                distribution['Sunflower'] += 1
            elif flower.type == 4:
                distribution['Coneflower'] += 1
            elif flower.type == 5:
                distribution['Blueberry'] += 1
        return distribution

    def PushUpdate(self):
        self.iterations += 1
        # Update flowers
        for i, flower in enumerate(self.flowers):
            status = flower.UpdateFlower(self.iterations)
            if status[0] == 1:
                self.AddFlower(status[1], 2, flower.type)
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
    def __init__(self, center, radius, birth, t='random', environment ='countryside', color='#FFC107', outer_color='#FFC107'):

        # Location
        self.x = center[0] + radius*np.random.uniform(-1, 1)
        self.y = center[1] + radius*np.random.uniform(-1, 1)
        self.location = [self.x, self.y]
        self.color = color
        
        # Type of flower
        types = [1, 2, 3, 4, 5] # [Lavender, Bee balm, Sunflower, Coneflower, Blueberry]      
        colors = ['purple', 'red', 'orange', 'pink', 'blue']
        
        if t == 'random':
            if environment == 'countryside':
                probabilities = [2, 2, 3, 5, 4]
                pSum = sum(probabilities)
                probabilities = [p/pSum for p in probabilities]
                self.type = np.random.choice(types, p=probabilities)
            elif environment == 'urban':
                probabilities = [5, 4, 3, 2, 1]
                pSum = sum(probabilities)
                probabilities = [p/pSum for p in probabilities]
                self.type = np.random.choice(types, p=probabilities)
            elif environment == 'agriculture':
                probabilities = [3, 1, 5, 1, 4]
                pSum = sum(probabilities)
                probabilities = [p/pSum for p in probabilities]
                self.type = np.random.choice(types, p=probabilities)
        else:
            self.type = t
        
        self.outer_color = colors[self.type - 1]

        # Characteristics of flowers
        life = 100
        pollen = 100
        if self.type == 1: # Lavender
            self.lifespan = 2*life
            self.pollen = pollen
        elif self.type == 2: # Bee balm
            self.lifespan = 2*life
            self.pollen = pollen
        elif self.type == 3: # Sunflower
            self.lifespan = life
            self.pollen = 4*pollen
        elif self.type == 4: # Coneflowers
            self.lifespan = life
            self.pollen = pollen
        elif self.type == 5: # Blueberry
            self.lifespan = life
            self.pollen = 4*pollen
    
        self.lifespan = 100
        self.creation = birth


    def __str__(self) -> str:
        if self.type == 1:
            return f'Lavender ({self.type}) at ({self.x:3.1f}, {self.y:3.1f})'
        elif self.type == 2:
            return f'Bee balm ({self.type}) at ({self.x:3.1f}, {self.y:3.1f})'
        elif self.type == 3:
            return f'Sunflower ({self.type}) at ({self.x:3.1f}, {self.y:3.1f})'
        elif self.type == 4:
            return f'Coneflower ({self.type}) at ({self.x:3.1f}, {self.y:3.1f})'
        elif self.type == 5:
            return f'Blueberry ({self.type}) at ({self.x:3.1f}, {self.y:3.1f})'

    def UpdateFlower(self, time) -> list:
        '''
        Update rules for flowers, 
        '''
        if self.pollen >= 200:
            self.pollen -= 200
            return [1, [self.x, self.y]]
        
        elif time - self.creation < self.lifespan:
            return [2, []]
        else:
            return [0, []]


class Nest:
    def __init__(self, center, radius) -> None:
        # Location
        self.x = center[0] + radius*np.random.uniform(-1, 1)
        self.y = center[1] + radius*np.random.uniform(-1, 1)
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

