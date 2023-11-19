import numpy as np



class Bee:
    def __init__(self, x, y, vision_angle=180, vision_range=40, angular_noise=0.01, speed=2, color="#ffd662"):
        self.x = x
        self.y = y
        self.path = [[self.x, self.y]]
        self.path_length = 100

        self.speed = speed
        self.orientation = np.random.uniform(0, 2 * np.pi)
        self.angular_noise = angular_noise

        self.visited_flowers = []
        self.visit_radius = 2
        self.short_memory = 10
        
        self.vision_angle = vision_angle
        self.vision_range = vision_range

        self.nectar = 0         # 0=hungry, 1 = fed?
        self.pollen = {}        # how much pollen and what kind

        self.color = color

        #self.vision_points = np.array([[10,0],[0,10]]) #coordinates of 2 points making a triangle if combined with position
        # add self.speed? (= norm of velocity)

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
                if len(self.visited_flowers) > self.short_memory:
                    self.visited_flowers.pop(0)
                else:
                    self.visited_flowers.append(nearest_flower)
        else:
            self.orientation = self.orientation + self.angular_noise * W 
        
        self.x += self.speed * np.cos(self.orientation)
        self.y += self.speed * np.sin(self.orientation)
        self.path.append([self.x, self.y])

        if len(self.path) > self.path_length:
            self.path.pop(0)

    def InFieldOfView(self, obj):
        # Check if the object is within the field of view and range
        direction_vector = np.array([obj.x - self.x, obj.y - self.y])
        distance = np.linalg.norm(direction_vector)

        if distance > 0:
            angle_to_obj = np.arctan2(direction_vector[1], direction_vector[0])
            angle_difference = np.abs(angle_to_obj - self.orientation)

            return angle_difference <= self.vision_angle / 2 and distance <= self.vision_range

        return False


 

    def find_flowers(self, nearby):   # Fix needed for when bee is pointing downwards
            # assuming "radius" in environment = "vision length" here
            vision_length = 20
            empty_flower = []
            found_flower = False

            bee_position = np.array([self.x,self.y])
            
            left_line = [bee_position,self.vision_points[0,:]]
            left_distances = left_line[0] - left_line[1]     # ∆x = bee x-left point x, ∆y = bee y -left point y
            left_slope = left_distances[1]/left_distances[0] # =∆y/∆x
            left_constant = self.y / (left_slope * self.x)        # m = y/kx
            
            right_line = [bee_position,self.vision_points[1,:]]
            right_distances = right_line[0] - right_line[1]     # ∆x = bee x-right point x, ∆y = bee y -right point y
            right_slope = right_distances[1]/right_distances[0] # =∆y/∆x
            right_constant = self.y / (right_slope * self.x)        # m = y/kx
            
            
            nearest_flower = [1000]
            
            for flower in nearby:
                x_flower, y_flower = flower[2], flower[3]
                distance = np.sqrt((self.x-x_flower)**2 + (self.y-y_flower)**2)   # remove later since circle already done in environemnt
                if distance > vision_length:  # if outside circle
                    continue
                if y_flower < left_slope * x_flower + left_constant: # if under left line
                    continue
                elif y_flower < right_slope * x_flower + right_constant: # if under right line
                    continue
                else:
                    if flower[0] < nearest_flower[0]:  #[0] --> distance
                        print(flower, '<', nearest_flower)
                        nearest_flower = flower
                        found_flower = True
                    else:
                        continue
                        
            if found_flower: 
                # go to coordinates of flower
                self.x,self.y = nearest_flower[2],nearest_flower[3]
                print('found flower',nearest_flower)
                empty_flower = nearest_flower
            
            return found_flower, empty_flower
        