import requests
import math
import pygame
import time

# Initialize pygame
pygame.init()

# Create a window to display the map
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set initial position of IMU to center of the window
x_pos = size[0] / 2
y_pos = size[1] / 2

# Set initial heading of IMU to 0 degrees
heading = 0

# Set time between data points
delta_t = 0.01

# Set initial accelerometer and gyroscope data
ax = 0
ay = 0
az = 0
gx = 0
gy = 0
gz = 0

# Set initial magnetometer data
mx = 0
my = 0
mz = 0

# Set initial lidar data
lidar_distance = 0

# Fetch the IMU data from the API endpoint
response = requests.get("http://192.168.4.1/imufull")
imu_data = response.json()

# Perform a complementary filter to combine accelerometer and gyroscope data
alpha = 0.98
while True:
    # Fetch the IMU data from the API endpoint
    response = requests.get("http://192.168.4.1/imufull")
    imu_data = response.json()

    # Extract the accelerometer data
    ax = imu_data["AccX"]
    ay = imu_data["AccY"]
    az = imu_data["AccZ"]
    # Extract the gyroscope data
    gx = imu_data["GyroX"]
    gy = imu_data["GyroY"]
    gz = imu_data["GyroZ"]
    # Extract the magnetometer data
    mx = imu_data["MagX"]
    my = imu_data["MagY"]
    mz = imu_data["MagZ"]
    # Extract the yaw, pitch, and roll data
    yaw = imu_data["Yaw"]
    pitch = imu_data["Pitch"]
    roll = imu_data["Roll"]

    # Use a complementary filter to combine the accelerometer and gyroscope data
    x_accel = ax * math.cos(pitch) + ay * math.sin(roll) * math.sin(pitch) + az * math.cos(roll) * math.sin(pitch)
    y_accel = ay * math.cos(roll) - az * math.sin(roll)
    x_velocity = x_velocity + x_accel * delta_t
    y_velocity = y_velocity + y_accel * delta_t
    x_pos = x_pos + x_velocity * delta_t
    y_pos = y_pos + y_velocity * delta_t

    # Use the magnetometer data to update the heading
    heading = math.atan2(my, mx)

    # Draw the walls usingthe lidar distance data
    lidar_distance = float(data["Distance"])
    x_wall = x_pos + lidar_distance * math.cos(heading)
    y_wall = y_pos + lidar_distance * math.sin(heading)
    pygame.draw.line(screen, (255, 0, 0), (x_pos, y_pos), (x_wall, y_wall), 5)

    # Update the IMU position based on the accelerometer data
    x_accel = float(data["AccX"])
    y_accel = float(data["AccY"])
    x_pos += x_accel * delta_t
    y_pos += y_accel * delta_t

    # Draw the IMU position on the screen
    pygame.draw.circle(screen, (0, 255, 0), (int(x_pos), int(y_pos)), 10)

    # Update the screen
    pygame.display.flip()

    # Wait for the next iteration
    time.sleep(delta_t)
    #Quit pygame
pygame.quit()
    

