import numpy as np


class Environment:
    '''
    The class acts as a framework for the environment and manages its content with initializing methods, adding methods and an update method.
    size = Size of the environment, used for both x and y axis.
    environmentType = Controlls the initialization of flowers to modell a specific environment type. Types available: 'countryside' (standard if not specified), 'urban', 'agriculture'
    '''
    def __init__(self, size, seasonLength, environmentType='countryside') -> None:
        '''
        Stores the content of the environment.
        '''
        print(f'\nAn environment has been created of type: \'{environmentType}\'')
        
        # Environment variables
        self.xLimit = size
        self.yLimit = size
        
        self.envType = environmentType
        self.seasonLength = seasonLength
        #self.monthLength = seasonLength//9

        # Flowers
        self.flowers = []
        self.newGeneration = []

        # Nests
        self.nests = []
        self.newNests = []
        self.radius = 0

    def InitializeFlowers(self, n) -> None:
        '''
        Initializes n number of flowers in the environment at time = 0
        '''

        if self.envType == 'countryside':
            self.radius = 500
            for i in range(n):
                center = [self.xLimit/2, self.yLimit/2]
                self.flowers.append(Flower(center, self.xLimit/2, 0, self.seasonLength, t='random', environment=self.envType))
        
        elif self.envType == 'urban':
            
            clusters = np.random.randint(30, 50)
            
            meanClusterSize = int(n/clusters)
            stdDev = 4 #int(meanClusterSize/10) 

            clusterSizes = np.random.normal(meanClusterSize, stdDev, clusters)
            clusterSizes = np.round(clusterSizes).astype(int)
            clusterSizes[-1] -= (np.sum(clusterSizes) - n)
            
            if clusterSizes[-1] < 0:
                clusterSizes.pop(clusters-1)
                clusters -= 1

            for i in range(clusters):

                center = [self.xLimit/2, self.yLimit/2]
                clusterCenterFlower = Flower(center, self.xLimit/2, 0, self.seasonLength, t='random', environment=self.envType)
                self.flowers.append(clusterCenterFlower)

                
                for _ in range(clusterSizes[i]-1):
                    self.AddFlower(clusterCenterFlower.location, 50, clusterCenterFlower.type, 0)        


        elif self.envType == 'agriculture':
            # Flower distribution
            types = [1, 2, 3, 4, 5]
            distribution = [3, 1, 5, 1, 4] # relation between flower
            dSum = sum(distribution)
            distribution = [d/dSum for d in distribution]
            iRange = [np.linspace(0, int(distribution[0]*n), num=int(distribution[0]*n)+1, dtype=int).tolist()]
            for i in range(1,len(distribution)):
                low = iRange[i-1][-1] + 1
                high = int(low + distribution[i]*n)
                tempRange = np.linspace(low, high, num=((high-low)+1), dtype=int).tolist()
                iRange.append(np.copy(tempRange).tolist())

            # Generate locations
            nRows = int(np.sqrt(n))
            nCols = int(np.sqrt(n))
            x = np.linspace(self.xLimit*0.05, self.xLimit*0.95, num=nRows)
            y = np.linspace(self.yLimit*0.05, self.yLimit*0.95, num=nCols)
            locations = [[i, j] for i in x for j in y]
            #print(locations)

            for i in range(len(locations)):
                for j in range(len(iRange)):
                    if i in iRange[j]:
                        self.AddFlower(locations[i], 0, types[j], 0)
        
        else:
            self.envType = 'countryside'
    
    def AddFlower(self, center, radius, flowerType, time) -> None:
        '''
        Method to add one or several flowers to the environment

        center = Around which coordinate the flower should be created
        radius = distance from center allowed
        flowerType = Which flower should be created
        '''

        self.flowers.append(Flower(center, radius, time, self.seasonLength, flowerType))
   
    def InitializeBeeNest(self, n) -> None:
        '''
        Initializes n number of nests in the environment at time = 0
        '''

        center = [self.xLimit/2, self.yLimit/2]
        
        for _ in range(n):
            self.nests.append(Nest(center, self.xLimit/4))

    def AddBeeNest(self, center, radius) -> None:
        '''
        Method to add one or several nests to the environment during the simulation

        center = Around which coordinate the nest should be created
        radius = Allowed distance from center
        '''
        
        self.nests.append(Nest(center, radius))

    def CreateNewGeneration(self, time) -> None:
        '''
        Method for creating the new generation of flowers. The method is called in the beginning of the new season in PushUpdate
        '''

        self.nests = []
        self.flowers = []

        for individual in self.newGeneration:
            self.AddFlower(individual[0], self.radius, individual[2], time)

        for nest in self.newNests:
            self.AddBeeNest(nest[0], nest[1])
        
        self.newGeneration = []
        self.newNests = []

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
    
    def AmountOfPollen(self) -> dict:
        distribution = {'Lavender': 0, 'Bee balm': 0, 'Sunflower': 0, 'Coneflower': 0, 'Blueberry': 0}
        for flower in self.flowers:
            if flower.type == 1:
                distribution['Lavender'] += flower.pollen
            elif flower.type == 2:
                distribution['Bee balm'] += flower.pollen
            elif flower.type == 3:
                distribution['Sunflower'] += flower.pollen
            elif flower.type == 4:
                distribution['Coneflower'] += flower.pollen
            elif flower.type == 5:
                distribution['Blueberry'] += flower.pollen
        return distribution

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

    def PushUpdate(self, time) -> None:
        '''
        Updates the content of the environment based on interactions in the simulation. Also manages the seasons.
        '''    

        # Update flowers
        for i, flower in enumerate(self.flowers):
            status, center = flower.UpdateFlower(time)
            if status == 1: # 1 = reproduce
                nFlowers = np.random.randint(1,flower.max_siblings) # how many "siblings"
                for _ in range(nFlowers): 
                    self.newGeneration.append([center, 40, flower.type]) #center, radius, type
            elif status == 2: # 2 = dead
                del self.flowers[i]

            if time % 2000 == 0: #regenerate pollen every 2000 timesteps so every day should this be less
                flower.pollen += flower.pollenRegeneration*2000

class Flower:
    '''
    The class represents a single flower with its attributes. Contains methods for updating.
    '''

    def __init__(self, center, radius, creation, seasonLength, t='random', environment ='countryside') -> None:

        # Location
        self.x = center[0] + radius * np.random.uniform(-1, 1)
        self.y = center[1] + radius * np.random.uniform(-1, 1)
        self.location = [self.x, self.y]
        self.reproduce = False

        # Type of flower
        types = [1, 2, 3, 4, 5] # [Lavender, Bee balm, Sunflower, Coneflower, Blueberry]      
        typeColors = ['purple', 'red', 'orange', 'pink', 'blue']
        
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
        pollenUnit = 1 #Assmue 1 unit 0.5 mm3
        pollenRegenerationUnit = 0.01

        if self.type == 1: # Lavender
            self.lifespan = life
            self.flowersPerStem = np.random.randint(5, 10)
            self.pollen = pollenUnit * self.flowersPerStem * 10 #Max 100 pollen
            self.pollenRegeneration = pollenRegenerationUnit * self.flowersPerStem * pollenUnit #Antar 10 stems per flower
            self.max_siblings = 5

        elif self.type == 2: # Bee balm
            self.lifespan = life
            self.flowersPerStem = np.random.randint(1, 5)
            self.pollen = pollenUnit * self.flowersPerStem * 10  #Max 50 pollen
            self.pollenRegeneration = pollenRegenerationUnit * self.flowersPerStem * pollenUnit
            self.max_siblings = 5

        elif self.type == 3: # Sunflower #NOTE: agriculture exclusive?
            self.lifespan = life//2
            self.flowersPerStem = 1
            self.pollen = 20 * pollenUnit * self.flowersPerStem  #Max 20 pollen
            self.pollenRegeneration = pollenRegenerationUnit * self.flowersPerStem * pollenUnit
            self.max_siblings = 6

        elif self.type == 4: # Coneflowers
            self.lifespan = life//2
            self.flowersPerStem = np.random.randint(1, 5)
            self.pollen = pollenUnit * self.flowersPerStem * 10  #Max 50 pollen
            self.pollenRegeneration = pollenRegenerationUnit * self.flowersPerStem * pollenUnit
            self.max_siblings = 5
        
        elif self.type == 5: # Blueberry
            self.lifespan = life //2
            self.flowersPerStem = np.random.randint(1, 5)
            self.pollen = pollenUnit * self.flowersPerStem * 5 #Max 25 pollen
            self.pollenRegeneration = pollenRegenerationUnit * self.flowersPerStem * pollenUnit
            self.max_siblings = 6
        
        self.color = typeColors[self.type - 1]

        self.creation = creation

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
        if self.reproduce == True:
            self.reproduce = False
            return [1, [self.x, self.y]]
        elif (time - self.creation) > self.lifespan:
            return [2, []]
        else:
            return [0, []]


class Nest:
    '''
    The class represents a single bee's nest in the environment and its attributes
    '''
    
    def __init__(self, center, radius) -> None:

        # Location
        self.x = center[0] + radius * np.random.uniform(-1, 1)
        self.y = center[1] + radius * np.random.uniform(-1, 1)
        self.location = [self.x, self.y]
        self.color = '#5C4033'
        self.pollen = 0
    
    def __str__(self) -> str:
        '''
        Method that allows for printing the nest. Not used in the simulation but for potential troubleshooting.
        '''

        return f'Nest at ({self.x}, {self.y})' 
