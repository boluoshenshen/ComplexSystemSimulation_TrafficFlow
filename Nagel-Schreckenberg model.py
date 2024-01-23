import numpy as np
import matplotlib.pyplot as plt

class Car:
    def __init__(self, position, max_speed=5, slowdown_prob=0.3, behavior='normal'):
        self.position = position
        self.speed = 0
        self.max_speed = max_speed
        self.slowdown_prob = slowdown_prob
        self.acceleration = 0.5 if behavior == 'reckless' else 0.05  # Adjusted for 0.1s time unit

    def update(self, road, delta_t):
        self.speed = min(self.speed + self.acceleration * delta_t, self.max_speed)
        distance = 0
        while road[(self.position + distance + 1) % len(road)] is None:
            distance += 1
        self.speed = min(self.speed, distance)
        if np.random.rand() < self.slowdown_prob:
            self.speed = max(self.speed - 1, 0)
        road[self.position] = None
        self.position = int(round((self.position + self.speed * delta_t) % len(road)))  # Adjusted for 0.1s time unit
        if self.position < len(road):
            road[self.position] = self

def car_count(time_step):
    if time_step < 3000 or time_step > 7000:  # Adjusted for 30000 time steps
        return [0] * 50 + [1] * 50
    else:
        return [0] * 30 + [1] * 20

def run_simulation(road_length, max_speed=5, slowdown_prob=0.3, behavior='normal', time_steps=30000):  # Adjusted for 30000 time steps
    positions = []
    for t in range(time_steps):
        road = [None] * road_length
        cars = []
        current_car_count = car_count(t)
        for car_type in current_car_count:
            if car_type == 0:
                behavior = 'normal'
            else:
                behavior = 'reckless'
            car = Car(np.random.randint(road_length), max_speed, slowdown_prob, behavior)
            while road[car.position] is not None:
                car.position = int(round((car.position + 1) % road_length))
            if car.position < len(road):
                road[car.position] = car
                cars.append(car)
        for car in cars:
            car.update(road, 0.1)  # Adjusted for 0.1s time unit
        positions.append([car.position for car in cars])
    return positions

road_length = 100
max_speed = 5
slowdown_prob = 0.3
time_steps = 30000  # Adjusted for 30000 time steps

positions = run_simulation(road_length, max_speed, slowdown_prob, time_steps=time_steps)

plt.figure(figsize=(15, 6))
for t, pos in enumerate(positions):
    plt.scatter([t] * len(pos), pos, color='blue', s=10)
plt.xlabel('Time Step')
plt.ylabel('Position on Road')
plt.title('Traffic Flow Simulation with Nagel-Schreckenberg Model')
plt.show()
