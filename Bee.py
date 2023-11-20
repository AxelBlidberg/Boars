import numpy as np

class Bee:
    def __init__(self, x, y, birth, vision_angle=180, vision_range=40, angular_noise=0.01, speed=2, color="#ffd662"):
        self.x = x
        self.y = y
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
        self.pollen = {}        # how much pollen and what kind


        self.color = color
        self.birth = birth

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
                nearest_flower.color="#2b79cb"
                if len(self.visited_flowers) > self.short_memory:
                    self.visited_flowers.pop(0)
                
        else:
            self.orientation = self.orientation + self.angular_noise * W 
        

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