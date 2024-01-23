# Translating the comments to English

import numpy as np
import matplotlib.pyplot as plt

# Parameters
road_length = 1000  # Length of the road
time_steps = 100  # Total number of time steps for the simulation
traffic_flow = [0] * 50 + [1] * 50  # First 50 time steps have no vehicles, the next 50 steps add one vehicle per step

# Vehicle class
class Vehicle:
    def __init__(self, behavior):
        self.position = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 1 if behavior == 'reckless' else 0.5
        self.behavior = behavior

    def update_position(self, vehicles):
        # Update speed and position based on driver behavior and position of vehicles ahead
        front_vehicle = next((v for v in vehicles if v.position > self.position), None)
        if front_vehicle and front_vehicle.position - self.position < 10:
            # If there is a vehicle ahead within a distance of 10, decelerate based on behavior
            self.speed = max(self.speed - (2 if self.behavior == 'reckless' else 1), 0)
        else:
            # Otherwise, accelerate, but do not exceed max speed
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        
        self.position += self.speed

# Vehicle class based on Intelligent Driver Model (IDM)
class IDMVehicle(Vehicle):
    def __init__(self, behavior):
        super().__init__(behavior)
        self.max_acceleration = 1.5  # Maximum acceleration
        self.desired_velocity = 5  # Desired velocity
        self.desired_time_headway = 1.5  # Desired time headway
        self.minimum_spacing = 2  # Minimum spacing when stationary
        self.comfortable_braking = 2  # Comfortable deceleration

    def calculate_acceleration(self, front_vehicle):
        # Safe distance
        delta_v = self.speed - (front_vehicle.speed if front_vehicle else 0)
        s_star = self.minimum_spacing + max(0, self.speed * self.desired_time_headway + self.speed * delta_v / (2 * np.sqrt(self.max_acceleration * self.comfortable_braking)))
        
        # Actual distance to the front vehicle
        s_alpha = (front_vehicle.position - self.position) if front_vehicle else float('inf')

        # IDM acceleration
        return self.max_acceleration * (1 - (self.speed / self.desired_velocity) ** 4 - (s_star / s_alpha) ** 2)

    def update_position(self, vehicles):
        front_vehicle = next((v for v in vehicles if v.position > self.position), None)
        self.speed = max(self.speed + self.calculate_acceleration(front_vehicle), 0)
        self.position += self.speed

# Re-simulate using the IDM model
vehicles = []
positions = [[] for _ in range(time_steps)] 

for t in range(time_steps):
    if traffic_flow[t] == 1:
        behavior = 'reckless' if np.random.rand() < 0.5 else 'cautious'
        vehicles.append(IDMVehicle(behavior))
    
    for vehicle in vehicles:
        vehicle.update_position(vehicles)
        positions[t].append(vehicle.position)

# Plot the simulation results
plt.figure(figsize=(15, 6))
for t in range(time_steps):
    plt.scatter([t] * len(positions[t]), positions[t], color='blue', s=10)
plt.xlabel('Time Step')
plt.ylabel('Position on Road')
plt.title('Traffic Flow Simulation with IDM')
plt.show()
