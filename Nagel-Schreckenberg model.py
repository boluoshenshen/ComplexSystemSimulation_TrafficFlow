import numpy as np
import random
import matplotlib.pyplot as plt

class Vehicle:
    def __init__(self, position, speed, behavior):
        self.position = position
        self.speed = speed
        self.behavior = behavior

v = 1000  # length of the road
T = 1000  # number of time steps
prob_create_peak = 0.8  # probability of creating a new vehicle during peak hours
prob_create_offpeak = 0.4  # probability of creating a new vehicle during off-peak hours
prob_slowdown_normal = 0.2  # probability of a normal driver slowing down
prob_slowdown_reckless = 0.1  # probability of a reckless driver slowing down
maxspeed = 4  # maximum speed of a vehicle
vehicles = [None for _ in range(v)]  # initialize the road with no vehicles

def get_prob_create(time_step):
    # determine the probability of creating a new vehicle based on the time step
    if 1000 <= time_step < 2000 or 7000 <= time_step < 8000:
        return prob_create_peak
    else:
        return prob_create_offpeak

def get_behavior():
    # determine the behavior of a new vehicle (reckless or normal)
    return 'reckless' if np.random.rand() < 0.5 else 'normal'

def update(vehicles):
    # update the positions and speeds of the vehicles
    new_vehicles = [None for _ in range(v)]
    for i in range(v):
        if vehicles[i] is not None:
            p = random.random()
            prob_slowdown = prob_slowdown_reckless if vehicles[i].behavior == 'reckless' else prob_slowdown_normal
            if p <= prob_slowdown and vehicles[i].speed > 0:
                vehicles[i].speed -= 1
            elif vehicles[i].speed < maxspeed:
                vehicles[i].speed += 1
            if i + vehicles[i].speed < v and vehicles[i].speed > 0:
                if vehicles[i + int(vehicles[i].speed)] is not None:  # If there is a vehicle in front
                    vehicles[i].speed = 0  # Stop the vehicle
                else:
                    vehicles[i].position += vehicles[i].speed
                    if vehicles[i].position >= v:
                        vehicles[i] = None
                    else:
                        new_vehicles[i + int(vehicles[i].speed)] = vehicles[i]
                        vehicles[i] = None
    p = random.random()
    if p <= get_prob_create(i) and new_vehicles[0] is None:
        new_vehicles[0] = Vehicle(0, random.randint(1, maxspeed), get_behavior())
    return new_vehicles

plt.figure(figsize=(15, 6))

for i in range(T):
    vehicles = update(vehicles)
    plt.scatter([i]*len([vehicle for vehicle in vehicles if vehicle is not None]), 
                [vehicle.position for vehicle in vehicles if vehicle is not None], color='blue', s=1)

plt.xlabel('Time Step')
plt.ylabel('Position on Road')
plt.title('Traffic Flow Over Time')
plt.show()
