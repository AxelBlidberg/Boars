import numpy as np


class Environment:
    def __init__(self, size, environmentType='countryside') -> None:
        print(f'\nAn environment has been created of type: \'{environmentType}\'')
        # Environment variables
        self.xLimit = size
        self.yLimit = size
        self.iterations = 0 #behövs eventuellt inte

        # Flowers
        self.newGeneration = []
        self.envType = environmentType
        self.flowers = []
        self.seasonLength = 1000

        # Nests
        self.nests = []

        # Hazards
        self.hazards = []

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

    def InitializeFlowers(self, n, time) -> None:
        '''
        Initializes n number of flowers in the environment
        '''

        if time > 1:
            ages_new_flowers = [time]*n
        else: 
            ages_new_flowers = np.random.randint(-200,0, size=n) # random birth-dates on first flowers


        if self.envType == 'countryside':
            for i in range(n):
                center = [self.xLimit/2, self.yLimit/2]
                self.flowers.append(Flower(center, self.xLimit/2, ages_new_flowers[i],self.seasonLength, t='random', environment=self.envType))   
            
        elif self.envType == 'urban':
            
            clusters = np.random.randint(3, 20)

            flowersPerCluster = int(n/clusters)  # alla cluster får samma antal blommor, men kanske göra en procentuell fördelning?

            for i in range(clusters):
                center = [self.xLimit/2, self.yLimit/2]
                clusterCenterFlower = Flower(center, self.xLimit/2, ages_new_flowers[i], self.seasonLength, t='random', environment=self.envType)
                self.flowers.append(clusterCenterFlower)

                for _ in range(flowersPerCluster):
                    self.AddFlower(clusterCenterFlower.location, 25, time, clusterCenterFlower.type)
        
        elif self.envType == 'agriculture':
            pass

        else:
            pass


        '''
        if time > 1:
            ages_new_flowers = [time]*n
        else: 
            ages_new_flowers = np.random.randint(-200,0, size=n) # random birth-dates on first flowers
        
        for i in range(n):
            center = [self.xLimit/2, self.yLimit/2]
            self.flowers.append(Flower(center, self.xLimit/2, ages_new_flowers[i],self.seasonLength, t='random', environment=self.envType))
        '''


    def CreateNewGeneration(self, time):
        for individual in self.newGeneration:
            self.AddFlower(individual[0], individual[1], time, individual[2])
        self.newGeneration = []

    def AddFlower(self, center, radius, time, flowerType) -> None:
        '''
        Method to add one or several flowers to the environment

        center = Around which coordinate the flower should be created
        radius = distance from center allowed
        flowerType = Which flower should be created
        '''
        self.flowers.append(Flower(center, radius, time, self.seasonLength,flowerType))

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

    def PushUpdate(self, time):
        self.iterations += 1
        # Update flowers
        for i, flower in enumerate(self.flowers):
            status = flower.UpdateFlower(time)
            if status[0] == 1:
                self.newGeneration.append([status[1], 10, flower.type])
                self.AddFlower(status[1], 10, time, flower.type)
            elif status[0] == 2:
                del self.flowers[i]
        if time % self.seasonLength == 0 and time != 0:
            self.flowers = []
            self.CreateNewGeneration(time)

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
    def __init__(self, center, radius, birth, seasonLength, t='random', environment ='countryside'):

        # Location
        self.x = center[0] + radius*np.random.uniform(-1, 1)
        self.y = center[1] + radius*np.random.uniform(-1, 1)
        self.location = [self.x, self.y]
        
        # Type of flower
        types = [1, 2, 3, 4, 5] # [Lavender, Bee balm, Sunflower, Coneflower, Blueberry]      
        possibleOuterColors = ['purple', 'red', 'orange', 'pink', 'blue']
        
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

        # Characteristics of flowers
        life = seasonLength
        pollen = 100
        if self.type == 1: # Lavender
            self.lifespan = life
            self.pollen = pollen
        elif self.type == 2: # Bee balm
            self.lifespan = life
            self.pollen = pollen
        elif self.type == 3: # Sunflower
            self.lifespan = int(life/2)
            self.pollen = 4*pollen
        elif self.type == 4: # Coneflowers
            self.lifespan = int(life/2)
            self.pollen = pollen
        elif self.type == 5: # Blueberry
            self.lifespan = int(life/2)
            self.pollen = 4*pollen
        
        
        #olika nyanser av gult i blomman för varje "100 pollen den har"
        self.possibleCenterColors = ["#FFFFCC", "#FFFF99", "#FFFF66", "#FFCC33", "#FFD700", "#B8860B", "#FAFAD2", "#EEE8AA", "#FFEB3B", "#FFC107"]
                
        self.centerColor = self.possibleCenterColors[min(self.pollen//100, len(self.possibleCenterColors) - 1)]
        
        #self.centerColor = '#FFC107'
        self.outerColor = possibleOuterColors[self.type - 1]

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
        if self.pollen > 500:
            self.pollen -= 500
            return [1, [self.x, self.y]]
        
        elif (time - self.creation) > self.lifespan:
            return [2, []]
        
        else:
            return [0, []]


class Nest:
    def __init__(self, center, radius) -> None:
        # Location
        self.x = center[0] + radius*np.random.uniform(-1, 1)
        self.y = center[1] + radius*np.random.uniform(-1, 1)
        self.location = [self.x, self.y]
        self.color='#5C4033'
        self.pollen = 0
    
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

