import numpy as np
import random

# Sonja o Lisa:
# RIP lista
# bee.n.o.eggs
# Densitet på blommor

#Vid tid:
#Hur många blommor ett bi pollinerar
#Hur många barn varje blomma får! 

class Swarm:
    '''
    The class acts as a framework for the swarm of bees and manages its content with initializing methods, adding methods and an update method.
    seasonLength = Duration of a season for when the bees are active
    '''
    def __init__(self, seasonLength) -> None:

        self.bees = []
        
        self.RIP_ages = [] # ages of dead bees
        self.RIP_number_of_eggs = [] # eggs of dead bees
        self.RIP_types = [] # type of the dead bees
        self.RIP_visitedflowers = []

        self.newNests = []
        self.newTraits  = []
        self.seasonLength = seasonLength 
        self.monthLength = self.seasonLength//3 
        self.weekLength = self.seasonLength //13 # = n.o. weeks in 3 months
        self.dayLength = self.seasonLength//90 #   
        self.activeBees = []     #     offspring pollen before = 400, 500, 800        pollen_capacity before = 300, 500   
        self.Beetypes = { 'Small Bee': {'speed': 1, 'pollen_capacity': 30,'vision_angle': 280 , 'vision_range':5, 'angular_noise': 0.45, 
                                        'color': "#ffd662", 'maxFlight': 250, 'offspringPollen' : 120, 'when_active' : [1,1,1], 'mean_age': self.weekLength*5.5,
                                        'type': 0, 'age_variation': int(self.weekLength*2.5), 'eat_pase':10, 'pollen_taken_perStem':10}, 
                    'Intermediate Bee': {'speed': 2, 'pollen_capacity': 40,'vision_angle': 280,'vision_range':20, 'angular_noise': 0.45,
                                        'color': "#FF6600",'maxFlight': 500 , 'offspringPollen' : 200, 'when_active' : [1,0,0],  'mean_age': self.dayLength*22 ,
                                        'type': 1, 'age_variation': int(self.dayLength*5), 'eat_pase':15, 'pollen_taken_perStem':15}} # eat_pase = how often bee eats
        
        self.total_egg = [0,0]  # For data collection
        self.totalDistribution = []
    
    def InitializeBees(self, n, nests, birth=0) -> None:
        bee_types = ['Small Bee', 'Intermediate Bee']
        
        for i in range(n):
            beetype = random.choice(bee_types)
            beeTraits = self.Beetypes[beetype]
            self.AddBee(nests[i], birth, beeTraits)

        self.totalDistribution = self.BeeDistribution(1)

    def AddBee(self, beenest, birth, beeTraits) -> None:
        self.bees.append(Bee(beenest, birth, beeTraits)) 
     
    
    def CreateNewGeneration(self, time, nests) -> None:
        for i in range(len(self.newNests)):
            self.AddBee(nests[i], time,self.newTraits[i])
        
        self.ActivateBees(time)
        self.totalDistribution = self.BeeDistribution(1)
    

    def BeeDistribution(self, historicDistribution) -> list:
        self.distribution = [0,0] 
        
        for bee in self.activeBees:
            if bee.type == 0:
                self.distribution[0] += 1
            elif bee.type == 1:
                self.distribution[1] += 1
        
        self.totalDistribution.append(self.distribution)

        if historicDistribution == 1:
            return self.totalDistribution
        
        return self.distribution
    
    def ActivateBees(self, time) -> None:
        '''
        Different types are active during different times of the season.
        '''
        self.activeBees = []
        current_month = time // self.monthLength % 3 # = n.o. simulated months

        #year = ['june','july','august']
        #print('Month:',year[current_month])
        #if current_month == 0 and time>self.seasonLength:
            #print('Happy new year!')

        for bee in self.bees:
            active_months = bee.Beetraits['when_active']

            if active_months[current_month] == 1:
                self.activeBees.append(bee)
                
    def PushUpdate(self, flowers, time) -> None:
        """
        Calls Update() or ReturnHome() and Eat(), and check if bee is full, starving or old for every active bee
        """
        if time % self.monthLength == 1: # every change of month
            self.ActivateBees(time)

        for i, bee in enumerate(self.activeBees):
            
            distance_to_home = np.linalg.norm([bee.home.x - bee.x, bee.home.y - bee.y])
            bee.Eat(time)

            if sum(bee.pollen.values()) > bee.pollen_capacity or distance_to_home > bee.max_flight:
                #if bee.turningHome:
                #     print('bee turns home')
                reproduce_true = bee.ReturnHome()

                if reproduce_true:
                    nest = bee.Reproduction()
                    self.newNests.append(nest)
                    self.newTraits.append(bee.Beetraits)
                    self.total_egg[bee.Beetraits["type"]] += 1

            
            elif sum(bee.pollen.values()) < 1:  #Kill bee if starving
                #print('RIP: bee died of starvation.') #Age:',bee_age)
                #print(f'RIP: {bee.type} has died of starvation.')

                self.RIP_ages.append((time-bee.birth)//self.dayLength) # save RIP data
                self.RIP_number_of_eggs.append(bee.number_of_eggs)
                self.RIP_types.append(bee.type)
                self.RIP_visitedflowers.append(bee.visitedflowers)
                
                self.bees.pop(i)
                self.activeBees.pop(i)
                del bee
                continue

            elif  time - bee.birth > bee.max_age:  # Kill bee if old
                #print(f'RIP: {bee.type} has died of age: {(time-bee.birth)//self.dayLength} days. Pollen levels: {bee.pollen}')
                #print('RIP: bee died of age:',(time-bee.birth)//self.dayLength,'days. Pollen levels:',bee.pollen)

                self.RIP_ages.append((time-bee.birth)//self.dayLength) # save RIP data
                self.RIP_number_of_eggs.append(bee.number_of_eggs)
                self.RIP_types.append(bee.type)
                self.RIP_visitedflowers.append(bee.visitedflowers)


                self.bees.pop(i)
                self.activeBees.pop(i)
                del bee
                continue
            
            else:
                bee.turningHome=True
                bee.Update(flowers)


class Bee:
    '''
    The class represents a single bee with its attributes.
    '''

    def __init__(self, nest, birth, beeTraits) -> None:
        self.x = nest.x
        self.y = nest.y
        self.home = nest
        self.path = [[self.x-0.2,self.y-0.2],[self.x, self.y]]
        self.path_length = 40

        self.Beetraits = beeTraits

        self.type = self.Beetraits["type"]
        self.speed = self.Beetraits["speed"]
        self.orientation = np.random.uniform(0, 2 * np.pi)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.angular_noise = self.Beetraits["angular_noise"]
        self.max_flight = self.Beetraits["maxFlight"] # max distance from nest
        self.required_pollen = self.Beetraits["offspringPollen"]

        self.visited_flowers = []
        self.visit_radius = 4
        self.short_memory = 10
        self.wait_counter = 0 #Initialize
        
        self.vision_angle = self.Beetraits["vision_angle"]
        self.vision_range = self.Beetraits["vision_range"]

        self.nectar = 0              # 0=hungry, 1 = fed?
        self.pollen = {1:10}        # how much pollen and what kind
        self.pollen_capacity = self.Beetraits["pollen_capacity"]

        self.color = self.Beetraits["color"]
        self.birth = birth
        self.waiting_constant = 0.5 # how long bees wait at flower depending on pollen #NOTE: Change to a reasonable value 
        self.chancePollination = 0.9 #NOTE: Change to a reasonable value 
        self.reproductionNestRadius = 40
        self.number_of_eggs = 0
        self.visitedflowers = 0


        self.eating_frequency = self.Beetraits["eat_pase"]
        self.turningHome =True #temporary
        self.pollen_taken_perStem = self.Beetraits['pollen_taken_perStem'] # How much pollen will bee take from one flower

        bee_age_mean = self.Beetraits['mean_age']
        age_variation = self.Beetraits['age_variation']
        self.max_age = np.random.normal(loc=bee_age_mean, scale=age_variation,size=1)[0] # each individual has "random" life-length

    def Update(self, flowers) -> None:
        """
        Bee movement, check for flowers, pollination
        """
        if self.wait_counter > 0:
            self.wait_counter -= 1
            return
            
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
                
                flowerType = nearest_flower.type 
                
                mean_take_pollen = self.pollen_taken_perStem * nearest_flower.flowersPerStem
                can_take = np.random.normal(loc=mean_take_pollen,scale=mean_take_pollen/3) # flat normal curve
                pollen_taken = int(min(nearest_flower.pollen, can_take))

                self.wait_counter = int(pollen_taken * self.waiting_constant) # adjust to fit timescale 
                self.visited_flowers.append(nearest_flower)

                #NOTE: Rimligt antagande om biet tar pollen och har pollen från samma blomma pollineras den
                if flowerType in self.pollen.keys():
                    r = np.random.random() 
                    if r < self.chancePollination:
                        nearest_flower.reproduce = True

                    self.pollen[flowerType] += pollen_taken
                else: 
                    self.pollen[flowerType] = pollen_taken

                nearest_flower.pollen -= pollen_taken
                self.visitedflowers += 1 

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


    def ReturnHome(self) -> bool:
        """
        Bee movement aims for home. Checks if bee is home yet. If nest.pollen > 200 > new egg. Called each timestep when bee is full. 
        """

        # self.turningHome = False # temporary to print when bee wants to go home
        distance_to_home = np.linalg.norm([self.home.x - self.x, self.home.y - self.y])

        if distance_to_home <= self.visit_radius: # If bee visits home
            food = sum(self.pollen.values())
            leave_home_ratio = 0.5 
            for key in self.pollen.keys(): # leave the same ratio of each pollen type
                self.pollen[key] = int(self.pollen[key] * (1-leave_home_ratio)) # bee loses pollen
            pollen_given = int(food * leave_home_ratio)
            self.home.pollen += pollen_given
            #print(self.home.pollen)
            #print('Bee pollen after',sum(self.pollen.values()))
            #print('Nest pollen after:',self.home.pollen)

            while self.home.pollen > self.required_pollen:
                self.home.pollen -= self.required_pollen
                #print('bee laid egg and pollen required was:',self.required_pollen)
                return True # reproduce

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
            return False # reproduce

    def Eat(self,time) -> None:
        # eats 1 random pollen every "self.eating_frequency" timestep  
        if time % self.eating_frequency == 0:
            if len(self.pollen) > 0:
                random_pollen_key = list(self.pollen.keys())[np.random.randint(0,len(self.pollen))]
                self.pollen[random_pollen_key] -= 1
                if self.pollen[random_pollen_key] < 1: # remove key if no pollen, so it cant get negative
                    self.pollen.pop(random_pollen_key) 

    def Reproduction(self) -> list:
        center = [self.x, self.y]
        nest = [center, self.reproductionNestRadius]
        self.number_of_eggs += 1
        #print('bee laid egg')
        #self.egg.append([center, radius]) # egg = [nest]
        return nest

    def InFieldOfView(self, obj) -> bool:
        direction_vector = np.array([obj.x - self.x, obj.y - self.y])
        distance = np.linalg.norm(direction_vector)
        
        if distance > 0:

            cos_angle = np.dot(self.velocity, direction_vector) / (np.linalg.norm(self.velocity) * distance)
            angle_threshold = np.cos(np.deg2rad(self.vision_angle / 2))
            if cos_angle >= angle_threshold and distance <= self.vision_range:
                return True

        return False