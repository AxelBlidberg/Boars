import numpy as np

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
        self.visit_radius = 4
        self.short_memory = 10
        
        self.vision_angle = vision_angle
        self.vision_range = vision_range

        self.nectar = 0         # 0=hungry, 1 = fed?
        self.pollen = pollen        # how much pollen and what kind

        self.color = color
        self.birth = birth

        bee_age_mean = 500
        self.max_age = np.random.normal(loc=bee_age_mean, scale=50,size=1)[0] # each individual has "random" life-length


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
                
                pollen_taken = np.random.randint(1, nearest_flower.pollen) # changed to min=1 to avoid negative food later

                if flowerType in self.pollen.keys():
                    
                    r = np.random.random()

                    if r < 1: #dummy value TODO: Fixa varierande reproduktion för varje blomma
                        pollen_given = 10
                        nearest_flower.pollen += pollen_given #self.pollen[flowerType] #Allt pollen ges från biet till blomman om pollen sker just nu
                        self.pollen[flowerType] -= pollen_given # bytte till 10 temporärt för att undvika problem med food / sonja
                        if self.pollen[flowerType] < 1: # remove key if no pollen, so it cant get negative
                            self.pollen.pop(flowerType)         
                    else:
                        self.pollen[flowerType] += pollen_taken #Biet tar en viss mängd pollen
                        nearest_flower.pollen -= pollen_taken

                        #Vill ta bort pollen från bieet om pollinering sker

                    #Pollinera eventuellt blomman

                else:
                    self.pollen[flowerType] = pollen_taken
                    
                #nearest_flower.pollen = nearest_flower.pollen - pollen_taken

                #color_scale = ["#FFFFCC", "#FFFF99", "#FFFF66", "#FFCC33", "#FFD700", "#B8860B", "#FAFAD2", "#EEE8AA", "#FFEB3B", "#FFC107"]
                
                #olika nyanser av gult i blomman för varje "100 pollen"
                #index = min(nearest_flower.pollen // 100, len(color_scale) - 1)

                index = min(nearest_flower.pollen//100, len(nearest_flower.possibleCenterColors) - 1)

                nearest_flower.centerColor = nearest_flower.possibleCenterColors[index]

                #nearest_flower.color= color_scale[nearest_flower.pollenAmount]   
                
                if len(self.visited_flowers) > self.short_memory:
                    self.visited_flowers.pop(0)
                
                          
                
        else:
            self.orientation = self.orientation + self.angular_noise * W 
        
        # eats x random pollen each timestep
        if len(self.pollen) > 0:
            eating_pase = 1          # pollen eaten per timestep
            random_pollen_key = list(self.pollen.keys())[np.random.randint(0,len(self.pollen))]
            self.pollen[random_pollen_key] -= eating_pase   
            if self.pollen[random_pollen_key] < 1: # remove key if no pollen, so it cant get negative
                self.pollen.pop(random_pollen_key) 

        self.x += self.speed * np.cos(self.orientation)
        self.y += self.speed * np.sin(self.orientation)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.path.append([self.x, self.y])

        if len(self.path) > self.path_length:
            self.path.pop(0)


    def ReturnHome(self):
        nearby_home = self.home if self.InFieldOfView(self.home) else False
        if nearby_home:
            distance_to_home = np.linalg.norm([self.home.x - self.x, self.home.y - self.y])
            if distance_to_home <= self.visit_radius:
                food = sum(self.pollen.values())
                print('bee went home to leave pollen')
                leave_home_ratio = 1/2
                for key in self.pollen.keys(): # leave the same ratio of each pollen type
                    self.pollen[key] = int(self.pollen[key] * (1-leave_home_ratio)) # bee loses pollen
                pollen_given = int(food * leave_home_ratio)
                self.home.pollen += pollen_given
                print('Bee pollen after',sum(self.pollen.values()))
                print('Nest pollen after:',self.home.pollen)
        
        W = np.random.uniform(-1/2, 1/2)
        direction_to_home = np.array([self.home.x - self.x, self.home.y - self.y])
        self.orientation = np.arctan2(direction_to_home[1], direction_to_home[0]) + self.angular_noise * W

         # eats x random pollen each timestep
        if len(self.pollen) > 0:
            eating_pase = 1          # pollen eaten per timestep
            random_pollen_key = list(self.pollen.keys())[np.random.randint(0,len(self.pollen))]
            self.pollen[random_pollen_key] -= eating_pase   
            if self.pollen[random_pollen_key] < 1: # remove key if no pollen, so it cant get negative
                self.pollen.pop(random_pollen_key) 

        self.x += self.speed * np.cos(self.orientation)
        self.y += self.speed * np.sin(self.orientation)
        self.velocity = [self.speed * np.cos(self.orientation), self.speed * np.sin(self.orientation)]
        self.path.append([self.x, self.y])

        if len(self.path) > self.path_length:
            self.path.pop(0)

    def InFieldOfView(self, obj):
        direction_vector = np.array([obj.x - self.x, obj.y - self.y])
        distance = np.linalg.norm(direction_vector)
        

        if distance > 0:

            cos_angle = np.dot(self.velocity, direction_vector) / (np.linalg.norm(self.velocity) * distance)
            angle_threshold = np.cos(np.deg2rad(self.vision_angle / 2))
            if cos_angle >= angle_threshold and distance <= self.vision_range:
                return True

        return False