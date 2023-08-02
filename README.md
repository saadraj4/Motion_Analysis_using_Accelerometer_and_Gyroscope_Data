# Motion_Analysis_using_Accelerometer_and_Gyroscope_Data
Motion Analysis using Accelerometer and Gyroscope Data. Python code for detecting motion events, estimating speed with Kalman Filter. Easily customizable.

## GitHub Repository: Motion Analysis using Accelerometer and Gyroscope Data

This repository contains Python code for analyzing motion data captured from accelerometer and gyroscope sensors. The code performs the following tasks:

1. **Internet Connection Check**: Verifies internet connectivity to install necessary libraries.
2. **Installing Required Packages**: Automatically installs required Python packages (`pandas` and `numpy`).
3. **Data Processing**: Reads accelerometer and gyroscope data from specified folders and calculates magnitude for each sensor reading.
4. **Motion Detection**: Detects start and end timestamps of motion events based on accelerometer and gyroscope thresholds.
5. **Speed Estimation**: Applies Extended Kalman Filter to estimate speed from the motion data.

### Requirements
1. Python (3.6+)
2. Internet connection (for library installation)

### Instructions:
1. Clone the repository to your local machine.
2. Ensure you have Python and pip installed.
3. Run the script: `python main.py`

### Configuration
1. Adjust thresholds, window size, and Kalman Filter parameters in the code as needed.
2. Adjust the threshold and window size for motion detection in the code.
3. Customize Extended Kalman Filter parameters (Q, R_accel, R_gyro, etc.) as needed.

### Dataset Folders:
The code assumes that the accelerometer and gyroscope data files are stored in folders named 'AA', 'BB', 'CC', ..., 'LL'. You can modify the list `folders` to match your data folder names.

### Output:
- Detected timestamps for motion start and end will be saved in CSV files: 'ball_static_timestamps folder.csv' and 'ball_moving_timestamps folder.csv', respectively, for each folder.
- Speed estimates will be saved in 'ball_speed_estimates folder.csv' for each folder.

**Note**: This code provides a basic implementation for motion analysis. Adjustments may be required based on the specific use case and sensor data characteristics.