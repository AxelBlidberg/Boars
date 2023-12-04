import numpy as np
import random

class Swarm:
    def __init__(self):
        self.bees = []
        self.newGeneration = []
        self.seasonLength = 900
        self.monthLength = self.seasonLength//9
        self.activeBees = []
        self.Beetypes = {'Small Bee': {'speed': 2, 'pollen_capacity': 300,'vision_angle': 280 , 'vision_range':40, 'angular_noise': 0.01, 
                                       'color': "#ffd662", 'maxFlight': 120, 'offspringPollen' : 400, 'when_active' : [0,0,0,1,1,1,1,0,0,0]}, # [mar, apr, may, jun, jul, sep, oct, nov]
                    'Intermediate Bee': {'speed': 4, 'pollen_capacity': 500,'vision_angle': 280,'vision_range':40, 'angular_noise': 0.01,
                                        'color': "#FF6600",'maxFlight': 180 , 'offspringPollen' : 500, 'when_active' : [1,1,1,1,0,0,0,0,0]},
                    'Large Bee': {'speed': 6, 'pollen_capacity': 1000,'vision_angle': 280,'vision_range':40, 'angular_noise': 0.01,
                                        'color': "#ffbc62",'maxFlight': 240, 'offspringPollen' : 800, 'when_active' : [0,1,1,1,0,1,1,1,0] }} 
    
    def InitializeBees(self, n, nests, birth=0):
        #Defining Beetype! Should this be moved to Simulation.py?
        bee_types = ['Small Bee', 'Intermediate Bee', 'Large Bee']
        
        for i in range(n):
            beetype = random.choice(bee_types)
            beetraits = self.Beetypes[beetype]
            self.AddBee(nests[i], birth, beetraits)

    def AddBee(self, beenest, birth,beetraits):
        for month in beetraits['when_active']:
            if month==0:
                birth+=self.monthLength
        self.bees.append(Bee(beenest, birth,beetraits)) 
    
    def CreateNewGeneration(self, newnests,parent_traits, time): #CreateNewGeneration(self.environment.nests,parent_type, 0)
        self.bees = []
        for i, nest in enumerate(newnests):
            #print(i)
            self.AddBee(nest, time,parent_traits[i])

    def BeeDistribution(self) -> dict:
        distribution = {'Small Bee': 0, 'Intermediate Bee': 0, 'Large Bee': 0}
        for bee in self.bees:
            if bee.type == 1:
                distribution['Small Bee'] += 1
            elif bee.type == 2:
                distribution['Intermediate Bee'] += 1
            elif bee.type == 3:
                distribution['Large Bee'] += 1
        return distribution
    
    def ActivateBees(self,time):
        """
        Different types are active during different times of the season.
        """
        self.activeBees = []
        current_month = time // self.monthLength % 9 # = n.o. simulated months

        year = ['mars','april','may','june','july','august','september','october','november']
        print('Month:',year[current_month])
        if current_month == 0 and time>self.seasonLength:
            print('Happy new year!')

        for bee in self.bees:
            active_months = bee.Beetraits['when_active']

            if active_months[current_month] == 1:
                self.activeBees.append(bee)
                

    def PushUpdate(self, flowers, time, angular_noise, vision_range, vision_angle):
        """
        Calls Update() or ReturnHome() and Eat(), and check if bee is full, starving or old for every active bee
        """
        if time % self.monthLength == 1: # every change of month
            self.ActivateBees(time)

        for bee_number, bee in enumerate(self.activeBees):

            bee.vision_angle = vision_angle
            bee.vision_range = vision_range
            bee.angular_noise = angular_noise
            
            distance_to_home = np.linalg.norm([bee.home.x - bee.x, bee.home.y - bee.y])

            # if full or flight distance too long
            if sum(bee.pollen.values()) > bee.pollen_capacity or distance_to_home > bee.max_flight:
                 if bee.turningHome:
                     #print('bee turns home')
                     pass
                 bee.ReturnHome() 
                 bee.Eat(time)
            
            elif sum(bee.pollen.values()) < 1:  # Kill bee if starving
                print('RIP: bee died of starvation.') #Age:',bee_age)
                self.bees.pop(bee_number)
                self.activeBees.pop(bee_number)
                del bee
                continue
            
            else:
                bee.turningHome=True
                bee.Update(flowers)
                bee.Eat(time)
            
            """
            elif  time - bee.birth > bee.max_age:  # Kill bee if old
                print('RIP: bee died of age:',time-bee.birth,'. Pollen levels:',bee.pollen)
                self.bees.pop(bee_number)
                self.activeBees.pop(bee_number)
                del bee
                continue
            """


class Bee:
    #def __init__(self, nest, birth, pollen_capacity=1000, vision_angle=180, vision_range=40, angular_noise=0.01, speed=2, color="#ffd662"):
    def __init__(self, nest, birth, beetraits):
        self.x = nest.x
        self.y = nest.y
        self.home = nest    # (object)
        self.path = [[self.x, self.y]]
        self.path_length = 40

        self.Beetraits = beetraits

        self.speed = self.Beetraits["speed"]
        self.orientation = np.random.uniform(0, 2 * np.pi)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.angular_noise = self.Beetraits["angular_noise"]
        self.max_flight = self.Beetraits["maxFlight"] # max distance from nest
        self.required_pollen = self.Beetraits["offspringPollen"]

        self.visited_flowers = []
        self.visit_radius = 4
        self.short_memory = 10
        
        self.vision_angle = self.Beetraits["vision_angle"]
        self.vision_range = self.Beetraits["vision_range"]

        self.nectar = 0              # 0=hungry, 1 = fed?
        self.pollen = {1:100}        # how much pollen and what kind
        self.pollen_capacity = self.Beetraits["pollen_capacity"]

        self.color = self.Beetraits["color"]
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

                index = int(min(nearest_flower.pollen//100, len(nearest_flower.possibleCenterColors) - 1))

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


        #nearby_home = self.home if self.InFieldOfView(self.home) else False

        self.turningHome=False # temporary to print when bee wants to go home
        #if nearby_home: # If bee sees home
        distance_to_home = np.linalg.norm([self.home.x - self.x, self.home.y - self.y])

        if distance_to_home <= self.visit_radius: # If bee visits home
            food = sum(self.pollen.values())
            leave_home_ratio = 0.5 
            for key in self.pollen.keys(): # leave the same ratio of each pollen type
                self.pollen[key] = int(self.pollen[key] * (1-leave_home_ratio)) # bee loses pollen
            pollen_given = int(food * leave_home_ratio)
            self.home.pollen += pollen_given
            #print('Bee pollen after',sum(self.pollen.values()))
            #print('Nest pollen after:',self.home.pollen)

            while self.home.pollen > self.required_pollen:
                self.Reproduction()
                self.home.pollen -= self.required_pollen
                print('bee laid egg and pollen required was:',self.required_pollen)
        
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