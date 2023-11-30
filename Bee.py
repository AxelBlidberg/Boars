import numpy as np

class Swarm:
    def __init__(self):
        self.bees = []
        self.newGeneration = []
        self.seasonLength = 1000
    
    def InitializeBees(self, n, nests, birth=0):
        for i in range(n):
            self.AddBee(nests[i], birth)

    def AddBee(self, beenest, birth):
        self.bees.append(Bee(beenest, birth))

    def CreateNewGeneration(self, beenest, time):
        self.bees = []
        for nest in beenest:
            self.AddBee(nest, time)
            
        #self.bees.egg = []
    
    def PushUpdate(self, flowers, time, angular_noise, vision_range, vision_angle):
        for bee in self.bees:
            full = 500
            bee.vision_angle = vision_angle
            bee.vision_range = vision_range
            bee.angular_noise = angular_noise
            
            if sum(bee.pollen.values()) > full:
                 bee.ReturnHome() # return to home if cannot carry more pollen
                 #print("Bee returning home!")
            else:
                bee.Update(flowers)
        
        #Göra en funktion reproduction som när ett bi lämnar pollen genererar 0-X antal offspring med en viss sannolikhet?
        #Där maximala antalet ägg beror på mängden pollen!!

        #print(time)

        #if time == self.seasonLength:
        #    print("New Bee Generation")
        #    self.CreateNewGeneration(time)


class Bee:
    def __init__(self, nest, birth, pollen={},vision_angle=180, vision_range=40, angular_noise=0.01, speed=2, color="#ffd662"):
        self.x = nest.x
        self.y = nest.y
        self.home = nest    # (object)
        self.path = [[self.x, self.y]]
        self.path_length = 100

        self.speed = speed
        self.orientation = np.random.uniform(0, 2 * np.pi)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.angular_noise = angular_noise

        self.visited_flowers = []
        self.visit_radius = 2
        self.short_memory = 10
        
        self.vision_angle = vision_angle
        self.vision_range = vision_range

        self.nectar = 0         # 0=hungry, 1 = fed?
        self.pollen = pollen        # how much pollen and what kind

        self.color = color
        self.birth = birth

        self.egg = []
        self.newhomes = []

        #bee_age_mean = 500
        #self.max_age = np.random.normal(loc=bee_age_mean, scale=50,size=1)[0] # each individual has "random" life-length

    def Update(self, flowers):
        # Angular noise to the direction
        W = np.random.uniform(-1/2, 1/2)

        # Get nearby flowers within the field of view and range excluding visited.
        nearby_flowers = [flower for flower in flowers if self.InFieldOfView(flower)]
        nearby_flowers = [flower for flower in nearby_flowers if flower not in self.visited_flowers]

        if nearby_flowers:
            nearest_flower = min(nearby_flowers, key=lambda flower: np.linalg.norm([flower.x - self.x, flower.y - self.y]))
            direction_to_nearest = np.array([nearest_flower.x - self.x, nearest_flower.y - self.y])
            self.orientation = np.arctan2(direction_to_nearest[1], direction_to_nearest[0]) + self.angular_noise * W

            distance_to_nearest = np.linalg.norm([nearest_flower.x - self.x, nearest_flower.y - self.y])

            if distance_to_nearest <= self.visit_radius:
                self.visited_flowers.append(nearest_flower)
                flowerType = nearest_flower.type 
                
                #WARN: Is it realistic that it can collect half of the pollen in the flower
                #This means that flower will never run out of pollen
                #TODO: Find a suitable value
                pollen_taken = np.random.randint(0, nearest_flower.pollen*0.5) 

                #NOTE: Rimligt antagande om biet tar pollen och har pollen från samma blomma pollineras den
                if flowerType in self.pollen.keys():
                    r = np.random.random() #NOTE: Probability can be added if needed
                    #NOTE: Prompt to pollinate
                    if r < 0.9:
                        nearest_flower.reproduce = True

                    self.pollen[flowerType] += pollen_taken
                
                else: 
                    self.pollen[flowerType] = pollen_taken

                nearest_flower.pollen -= pollen_taken

                index = min(nearest_flower.pollen//100, len(nearest_flower.possibleCenterColors) - 1)

                nearest_flower.centerColor = nearest_flower.possibleCenterColors[index]

                #nearest_flower.color= color_scale[nearest_flower.pollenAmount]   
                
                if len(self.visited_flowers) > self.short_memory:
                    self.visited_flowers.pop(0)
                
        else:
            self.orientation = self.orientation + self.angular_noise * W 
        
        # eats x random pollen each timestep

        """
        if len(self.pollen) > 0:
            eating_pase = 1          # pollen eaten per timestep
            random_pollen_key = list(self.pollen.keys())[np.random.randint(0,len(self.pollen))]
            self.pollen[random_pollen_key] -= eating_pase   
            if self.pollen[random_pollen_key] < 1: # remove key if no pollen, so it cant get negative
                self.pollen.pop(random_pollen_key) 
        """
        self.x += self.speed * np.cos(self.orientation)
        self.y += self.speed * np.sin(self.orientation)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.path.append([self.x, self.y])

        if len(self.path) > self.path_length:
            self.path.pop(0)


    def ReturnHome(self): #Återvänder endast hem om den ser sitt hem?
        nearby_home = self.home if self.InFieldOfView(self.home) else False
        required_pollen = 600
        if nearby_home:
            distance_to_home = np.linalg.norm([self.home.x - self.x, self.home.y - self.y])
            if distance_to_home <= self.visit_radius:
                food = sum(self.pollen.values())
                print('bee went home to leave pollen')
                leave_home_ratio = 1 #Leaving all pollen
                for key in self.pollen.keys(): # leave the same ratio of each pollen type
                    self.pollen[key] = int(self.pollen[key] * (1-leave_home_ratio)) # bee loses pollen
                pollen_given = int(food * leave_home_ratio)
                self.home.pollen += pollen_given
                print('Bee pollen after',sum(self.pollen.values()))
                print('Nest pollen after:',self.home.pollen)

                if self.home.pollen > required_pollen:
                    self.Reproduction()
                    self.home.pollen -= required_pollen
        
        W = np.random.uniform(-1/2, 1/2)
        direction_to_home = np.array([self.home.x - self.x, self.home.y - self.y])
        self.orientation = np.arctan2(direction_to_home[1], direction_to_home[0]) + self.angular_noise * W

        """    
         # eats x random pollen each timestep
        if len(self.pollen) > 0:
            eating_pase = 1          # pollen eaten per timestep
            random_pollen_key = list(self.pollen.keys())[np.random.randint(0,len(self.pollen))]
            self.pollen[random_pollen_key] -= eating_pase   
            if self.pollen[random_pollen_key] < 1: # remove key if no pollen, so it cant get negative
                self.pollen.pop(random_pollen_key) 
        """
        self.x += self.speed * np.cos(self.orientation)
        self.y += self.speed * np.sin(self.orientation)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.path.append([self.x, self.y])

        if len(self.path) > self.path_length:
            self.path.pop(0)
    
    def Reproduction(self):
        center = [self.x, self.y]
        radius = 10
        
        self.egg.append([center, radius])

    def InFieldOfView(self, obj):
        direction_vector = np.array([obj.x - self.x, obj.y - self.y])
        distance = np.linalg.norm(direction_vector)
        

        if distance > 0:

            cos_angle = np.dot(self.velocity, direction_vector) / (np.linalg.norm(self.velocity) * distance)
            angle_threshold = np.cos(np.deg2rad(self.vision_angle / 2))
            if cos_angle >= angle_threshold and distance <= self.vision_range:
                return True

        return False