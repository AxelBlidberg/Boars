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

    """""
    def CreateNewGeneration(self, nests, time): 
        for egg in newBorn.values():
            center = egg[0]
            radis = egg[1]
            for _ in range(nEggs):
                nest = nests[np.random.randint(0,len(nests))] # right now in random nests
                self.AddBee(nest, time)
    """    
    
    def CreateNewGeneration(self, newnests, time): 
        self.bees = []
        for nest in newnests:
            self.AddBee(nest, time)
            

    def PushUpdate(self, flowers, time, angular_noise, vision_range, vision_angle):
        """
        Calls Update() and Eat(), and check if bee is full, starving or old for every bee
        """
        for bee_number, bee in enumerate(self.bees):
            bee.vision_angle = vision_angle
            bee.vision_range = vision_range
            bee.angular_noise = angular_noise
            
            if sum(bee.pollen.values()) > bee.pollen_capacity:
                 if bee.turningHome:
                     #print('turning home, bee nr:', bee_number)
                     pass
                 bee.ReturnHome() # return to home if cannot carry more pollen
                 bee.Eat(time)
            
            elif sum(bee.pollen.values()) < 1:  # Kill bee if starving
                print('RIP: bee died of starvation.') #Age:',bee_age)
                self.bees.pop(bee_number)
                del bee
                continue
            
            elif  time - bee.birth > bee.max_age:  # Kill bee if old
                print('RIP: bee died of age:',time-bee.birth,'. Pollen levels:',bee.pollen)
                self.bees.pop(bee_number)
                del bee
                continue

            else:
                bee.turningHome=True
                bee.Update(flowers)
                bee.Eat(time)


class Bee:
    def __init__(self, nest, birth, pollen_capacity=1000, vision_angle=180, vision_range=40, angular_noise=0.01, speed=2, color="#ffd662"):
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
        self.pollen = {1:100}        # how much pollen and what kind
        self.pollen_capacity = pollen_capacity

        self.color = color
        self.birth = birth

        self.egg = []
        self.newhomes = []

        self.eating_frequency = 10
        self.turningHome =True #temporary

        bee_age_mean = 700
        self.max_age = np.random.normal(loc=bee_age_mean, scale=50,size=1)[0] # each individual has "random" life-length

    def Update(self, flowers):
        """
        Bee movement, check for flowers, pollination
        """
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
                # Caused bees to starve quickly, changed to: min(can_take, previous)
                #TODO: Find a suitable value

                can_take = np.random.normal(loc=100,scale=10)
                pollen_taken = int(min(nearest_flower.pollen*0.5, can_take))

                #pollen_taken = np.random.randint(0, nearest_flower.pollen*0.5) 

                #NOTE: Rimligt antagande om biet tar pollen och har pollen från samma blomma pollineras den
                if flowerType in self.pollen.keys():
                    r = np.random.random() #NOTE: Probability can be added if needed
                    #NOTE: Prompt to pollinate
                    chancePollination = 0.9
                    if r < chancePollination:
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
        
        # Bee moves
        self.x += self.speed * np.cos(self.orientation)
        self.y += self.speed * np.sin(self.orientation)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.path.append([self.x, self.y])

        if len(self.path) > self.path_length:
            self.path.pop(0)


    def ReturnHome(self): # Återvänder endast hem om den ser sitt hem? svar: nej, det va lite otydlilgt men nu la jag till kommentarer så man nog fattar
        """
        Bee movement aims for home. Checks if bee is home yet. If nest.pollen > 200 > new egg. Called each timestep when bee is full. 
        """

        nearby_home = self.home if self.InFieldOfView(self.home) else False
        required_pollen = 100 # To reproduce
        self.turningHome=False # temporary to print when bee wants to go home
        if nearby_home: # If bee sees home
            distance_to_home = np.linalg.norm([self.home.x - self.x, self.home.y - self.y])
            if distance_to_home <= self.visit_radius: # If bee visits home
                food = sum(self.pollen.values())
                #print('bee went home to leave pollen')
                leave_home_ratio = 0.5 
                for key in self.pollen.keys(): # leave the same ratio of each pollen type
                    self.pollen[key] = int(self.pollen[key] * (1-leave_home_ratio)) # bee loses pollen
                pollen_given = int(food * leave_home_ratio)
                self.home.pollen += pollen_given
                #print('Bee pollen after',sum(self.pollen.values()))
                #print('Nest pollen after:',self.home.pollen)

                while self.home.pollen > required_pollen:
                    self.Reproduction()
                    self.home.pollen -= required_pollen
                    print('bee laid egg')
        
        # Bee flies towards home:
        W = np.random.uniform(-1/2, 1/2)  
        direction_to_home = np.array([self.home.x - self.x, self.home.y - self.y])
        self.orientation = np.arctan2(direction_to_home[1], direction_to_home[0]) + self.angular_noise * W
        self.x += self.speed * np.cos(self.orientation)
        self.y += self.speed * np.sin(self.orientation)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.path.append([self.x, self.y])

        if len(self.path) > self.path_length:
            self.path.pop(0)
            
    def Eat(self,time):
        # eats 1 random pollen every "self.eating_frequency" timestep  
        if time % self.eating_frequency == 0:
            if len(self.pollen) > 0:
                random_pollen_key = list(self.pollen.keys())[np.random.randint(0,len(self.pollen))]
                self.pollen[random_pollen_key] -= 1
                if self.pollen[random_pollen_key] < 1: # remove key if no pollen, so it cant get negative
                    self.pollen.pop(random_pollen_key) 

    def Reproduction(self):
        center = [self.x, self.y]
        radius = 20
        
        self.egg.append([center, radius]) # egg = [nest]

    def InFieldOfView(self, obj):
        direction_vector = np.array([obj.x - self.x, obj.y - self.y])
        distance = np.linalg.norm(direction_vector)
        
        if distance > 0:

            cos_angle = np.dot(self.velocity, direction_vector) / (np.linalg.norm(self.velocity) * distance)
            angle_threshold = np.cos(np.deg2rad(self.vision_angle / 2))
            if cos_angle >= angle_threshold and distance <= self.vision_range:
                return True

        return False