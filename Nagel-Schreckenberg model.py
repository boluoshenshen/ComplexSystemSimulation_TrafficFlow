

import numpy as np
import matplotlib.pyplot as plt

class Car:
    def __init__(self, position, max_speed=5, slowdown_prob=0.3, behavior='normal'):
        self.position = position
        self.speed = 0
        self.max_speed = max_speed
        self.slowdown_prob = slowdown_prob
        self.acceleration = 1 if behavior == 'reckless' else 0.5

    def update(self, road, delta_t):
        # Accelerate the car based on its acceleration value
        self.speed = min(self.speed + self.acceleration, self.max_speed)

        # Slow down to avoid collision with the car ahead
        distance = 0
        while road[(self.position + distance + 1) % len(road)] is None:
            distance += 1
        self.speed = min(self.speed, distance)

        # Random slowdown with a given probability
        if np.random.rand() < self.slowdown_prob:
            self.speed = max(self.speed - 1, 0)

        # Move the car forward based on its updated speed
        road[self.position] = None
        self.position = (self.position + self.speed) % len(road)
        road[self.position] = self

def run_simulation(road_length, car_count, max_speed=5, slowdown_prob=0.3, behavior='normal', time_steps=60):
    road = [None] * road_length
    cars = []
    if isinstance(car_count, int):
        car_count = [1] * car_count  
    for car_type in car_count:
        if car_type == 0:
            behavior = 'normal'
        else:
            behavior = 'reckless'
        car = Car(np.random.randint(road_length), max_speed, slowdown_prob, behavior)
        while road[car.position] is not None:
            car.position = (car.position + 1) % road_length
        road[car.position] = car
        cars.append(car)

    positions = []
    for _ in range(time_steps):
        for car in cars:
            car.update(road, 1)
        positions.append([car.position for car in cars])
    
    return positions

# Parameters
road_length = 100 # Length of the road
car_count = 30 
max_speed = 5
slowdown_prob = 0.3  # Probability of random slowdown
time_steps = 60

positions = run_simulation(road_length, car_count, max_speed, slowdown_prob, time_steps=time_steps)

# Plot
plt.figure(figsize=(15, 6))
for t, pos in enumerate(positions):
    plt.scatter([t] * len(pos), pos, color='blue', s=10)  # s controls the size of the points

plt.xlabel('Time Step')
plt.ylabel('Position on Road')
plt.title('Traffic Flow Simulation with Nagel-Schreckenberg Model')
plt.show()





