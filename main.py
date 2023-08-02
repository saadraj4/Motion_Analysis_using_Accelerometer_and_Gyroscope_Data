import os
import platform
import subprocess
import socket
import time


# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def is_internet_connected():
    try:
        # Attempt to create a socket connection to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        print(f"\033[32mInternet connection is established\033[0m")
        return True
    except OSError:
        # If the connection attempt fails, it means the internet is not connected
        print(f"\033[31mInternet is not connected,Please try again!\033[0m")
        return False


# Installing required packages and libraries
if is_internet_connected():
    time.sleep(2)
    clear_screen()
    # Installing required packages and Libraries
    required_packages = ['pandas', 'numpy']
    for package in required_packages:
        try:
            subprocess.check_call(['pip', 'install', package], bufsize=0)
            print(f"\033[32mSuccessfully installed {package}\033[0m")
            time.sleep(2)
            # Clear the screen after installation
            clear_screen()
        except subprocess.CalledProcessError:
            print(f"\033Failed to install {package}\033[0m")
            exit()
else:
    exit()

import pandas as pd
import numpy as np


# Read the data from file
def readData(folder):
    accel_data = pd.read_csv(rf".\{folder}\AD.csv")
    gyro_data = pd.read_csv(rf".\{folder}\GD.csv")
    return accel_data, gyro_data


# Sample code to process accelerometer data
# Calculate magnitude for each row in accelerometer data
def calculateAccelMagnitude(row):
    return (row['X [g]'] ** 2 + row['Y [g]'] ** 2 + row['Z [g]'] ** 2) ** 0.5


# Calculate magnitude for each row in gyroscope data
def calculateGyroMagnitude(row):
    return (row['X [°/s]'] ** 2 + row['Y [°/s]'] ** 2 + row['Z [°/s]'] ** 2) ** 0.5


# Extended Kalman filter function
def extended_kalman_filter(speed_estimate, error_covariance, measurement_accel, measurement_gyro, timestamp, Q):
    # Prediction step
    speed_prediction = speed_estimate
    error_prediction = error_covariance + Q

    # Update step for accelerometer data
    K_accel = error_prediction / (error_prediction + R_accel)
    speed_estimate = speed_prediction + K_accel * (measurement_accel - speed_prediction)
    error_covariance = (1 - K_accel) * error_prediction

    # Update step for gyroscope data
    K_gyro = error_covariance / (error_covariance + R_gyro)
    speed_estimate = speed_estimate + K_gyro * (measurement_gyro - speed_estimate)
    error_covariance = (1 - K_gyro) * error_covariance

    return speed_estimate, error_covariance, timestamp


def shotStart(data, accel_thresh, gyro_thresh):
    shot_timestamps = []  # List to store the timestamps of detected shot events
    accel = data['Acceleration Magnitude [g]']
    gyro = data['Angular Velocity Magnitude [°/s]']
    time = data['Time [s]']
    for i in range(len(data)):
        if accel[i] > accel_thresh and gyro[i] > gyro_thresh:
            time[i] = round(time[i], 1)
            if time[i] not in shot_timestamps:
                shot_timestamps.append(time[i])

    return shot_timestamps


def shotEnd(data, accel_thresh, gyro_thresh):
    shot_timestamps = []  # List to store the timestamps of detected shot events
    accel = data['Acceleration Magnitude [g]']
    gyro = data['Angular Velocity Magnitude [°/s]']
    time = data['Time [s]']
    for i in range(len(data)):
        if accel[i] < accel_thresh and gyro[i] < gyro_thresh:
            time[i] = round(time[i], 1)
            if time[i] not in shot_timestamps:
                shot_timestamps.append(time[i])

    return shot_timestamps


def shotSpeed(data, initial_speed_estimate, P, Q):
    # Apply Extended Kalman filter to estimate speed for each measurement
    for i in range(len(data)):
        accel_measurement = data['Acceleration Magnitude [g]']
        gyro_measurement = data['Angular Velocity Magnitude [°/s]']
        timestamp = data['Time [s]']  # Assuming the timestamps are the same in both datasets

        # Apply Extended Kalman filter for both accelerometer and gyroscope data
        initial_speed_estimate, P, timestamp = extended_kalman_filter(
            initial_speed_estimate, P, accel_measurement[i], gyro_measurement[i], timestamp[i], Q
        )

        estimated_speeds.append((initial_speed_estimate, timestamp))

    speed_data_dict = {}
    for speed, timestamp in estimated_speeds:
        speed_data_dict[timestamp] = speed
    return speed_data_dict


# Driver code

# Dataset folders
folders = ['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK', 'LL']

# Define threshold and window size (You may need to adjust these values)
accel_threshold = 3  # Replace with your desired threshold for acceleration
gyro_threshold = 80  # Replace with your desired threshold for angular velocity
window_size = 10  # Replace with the desired window size in data points

# Extended Kalman filter parameters
Q = 0.001  # Process covariance
R_accel = 0.1  # Accelerometer measurement covariance
R_gyro = 1.0  # Gyroscope measurement covariance
# Initial state (initial speed estimate)
initial_speed_estimate = 0.0
# Initial error covariance
P = 1.0
# State transition matrix (identity matrix for this simple example)
F = np.eye(1)
# Kalman gain
K = 0.0
# List to store the speed
estimated_speeds = []
for folder in folders:
    accel_data, gyro_data = readData(folder)

    # Calculate magnitude for each row in accelerometer data and store in a new column
    accel_magnitude = accel_data['Acceleration Magnitude [g]'] = accel_data.apply(calculateAccelMagnitude, axis=1)
    # Calculate magnitude for each row in gyroscope data and store in a new column
    gyro_magnitude = gyro_data['Angular Velocity Magnitude [°/s]'] = gyro_data.apply(calculateGyroMagnitude, axis=1)

    # Create new DataFrames with only timestamp and magnitude values
    accel_magnitude_df = accel_data[['Time [s]', 'Acceleration Magnitude [g]']]
    gyro_magnitude_df = gyro_data[['Time [s]', 'Angular Velocity Magnitude [°/s]']]
    # Merge the magnitude DataFrames based on timestamp (inner join)
    merged_data_df = pd.merge(accel_magnitude_df, gyro_magnitude_df, on='Time [s]', suffixes=('_accel', '_gyro'))

    # Testing the methods
    timestamps_end = shotEnd(merged_data_df, accel_threshold, gyro_threshold)
    end_df = pd.DataFrame({'Timestamps': timestamps_end})
    end_df.to_csv(f'.\{folder}\/ball_static_timestamps {folder}.csv', index=False)

    timestamps_start = shotStart(merged_data_df, accel_threshold, gyro_threshold)
    start_df = pd.DataFrame({'Timestamps': timestamps_start})
    start_df.to_csv(f'.\{folder}\/ ball_moving_timestamps {folder}.csv', index=False)

    speed_dict = shotSpeed(merged_data_df, initial_speed_estimate, P, Q)
    speed_df = pd.DataFrame(speed_dict.items(), columns=['Timestamps', 'Speed [g/s]'])
    speed_df.to_csv(f'.\{folder}\/ball_speed_estimates {folder}.csv', index=False)

print("\033[32mData saved to csv Files in respective folder\033[0m")
