import numpy as np

class Environment:
    def __init__(self, size) -> None:
        self.size = size
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
        for _ in range(n):
            center = [self.xLimit/2, self.yLimit/2]
            self.flowers.append(Flower(center, self.xLimit/2, self.iterations))

    def AddFlower(self, center, radius):
        '''
        Method to add one or several flowers to the environment

        n = Number of flowers to add
        '''
        self.flowers.append(Flower(center, radius))

    def AddBeeNest(self, n):
        '''
        Method to add one or several nests to the environment

        n = Number of nests to add
        size = Size of the environment for correct placement of flowers
        '''
        for _ in range(n):
            self.nests.append(Nest(self.xLimit))

    def ExportContent(self):
        '''
        Exports a list of the format [class, 'Type', x, y] ex: ['flower', 1, x, y]
        '''
        content = []

        for flower in self.flowers:
            content.append(['flower', flower.type, flower.x, flower.y])
        
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

    def Interaction(self, type, x, y):
        pass
        if type == 'flower':
            for flower in self.flowers:
                if flower.x == x and flower.y == y:
                    pass
                pass     

class Flower:
    def __init__(self, center, radius, birth) -> None:

        # Add control to ensure location is within environment


        self.x = center[0] + radius*np.random.randn()
        self.y = center[1] + radius*np.random.randn()
  
        self.type = np.random.randint(1, 5)
        self.flowersize = np.random.randint(1, 5)

        self.nectarAmount = np.random.randint(1,10)

        self.pollen = {f'{i}': 0 for i in range(1,6)}

        self.lifespan = 100
        self.creation = birth
        

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
        
    
    def GetNectarAmount(self):
        return self.nectarAmount

    def GetLocation(self) -> list:
        '''
        Returns the coordinates of a specific flower 
        '''
        return [self.x, self.y]
    
    def GetType(self):

        return self.type
    
    def GetSize(self):
        return self.flowersize
    
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
    def __init__(self, envsize) -> None:

        self.x = envsize*np.random.rand()
        self.y = envsize*np.random.rand()
    

    def GetLocation(self) -> list:
        '''
        Returns the coordinates of a nest
        '''
        return [self.x, self.y]
    

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



# def PlotFunction(data):
#     '''
#     Temporary function for plotting the environment. Takes a special formatted list obtained from the ExportContent method in the Environment class.
#     '''
#     types = [item[1] for item in data]
#     x_values = [item[2] for item in data]
#     y_values = [item[3] for item in data]

#     unique_types = set(types)
#     color_map = {t: i for i, t in enumerate(unique_types)}
#     colors = [color_map[t] for t in types]

#     plt.scatter(x_values, y_values, c=colors, cmap='viridis', s=50, alpha=0.8, label=types)
#     plt.xlabel('X-axis')
#     plt.ylabel('Y-axis')
#     plt.title('Scatter Plot with Colors')
#     plt.show()



#test = Environment(100)

#test.InitializeFlowers(10)

#neighbors = test.GetSurroundings([5,5], 5)
#A = test.ExportContent()
#test.PushUpdate()

#PlotFunction(A)

