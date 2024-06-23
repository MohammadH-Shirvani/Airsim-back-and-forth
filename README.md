# AirSim Multirotor Back-and-Forth Movement

This repository contains code to move a drone back and forth at multiple altitudes using the AirSim plugin in Unreal Engine. The drone is flown in the [Downtown West](https://www.unrealengine.com/marketplace/en-US/product/6bb93c7515e148a1a0a0ec263db67d5b) environment, and the path is plotted in XYZ coordinates.
This project is part of a larger effort to perform 3D reconstruction using images captured by the drone. The back-and-forth flight path is designed to capture a comprehensive set of images that can be used to reconstruct a 3D model of the environment.

## Project Structure

- `src/`: Contains the path code for moving the drone.
  - `path_code.py`: Script to move the drone back and forth at multiple altitudes.
- `scripts/`: Contains scripts for additional functionalities such as plotting.
  - `plot_path_xyz.py`: Script to plot the drone's path in XYZ coordinates.

## Requirements

- [AirSim](https://github.com/microsoft/AirSim)
- [Unreal Engine](https://www.unrealengine.com/)
- Python 3.x
- Required Python packages:
  - `matplotlib`
  - `airsim`

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/airsim-drone-back-and-forth.git
   cd airsim-drone-back-and-forth

2. Install the required Python packages:
   ```sh
   pip install matplotlib airsim

## Usage
1. Preparing the Environment
   Place the Drone:
   Open your Unreal Engine project and place the drone at the starting point of the building where you want the path to begin.
   Play the Environment:
   Start the environment in Unreal Engine by clicking the "Play" button. Ensure that the AirSim plugin is active and connected.
1. Run the code:
   Navigate to the src directory and run the path code script:
   ```sh
   cd src
   python path_code.py
2. Plot the path:
   Ensure the airsim_rec.txt file is correctly placed in the directory. The airsim_rec.txt file is used to record the drone's path during the simulation. It
   is expected to be
   located in the settings directory. This file contains the recorded drone path data required for plotting.
   ```sh
   cd scripts
   python plot_path_xyz.py
