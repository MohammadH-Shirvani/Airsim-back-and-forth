# AirSim Multirotor Back-and-Forth Movement

This repository contains code that utilizes the AirSim plugin within Unreal Engine to control an aerial robot, enabling it to move back and forth at multiple, overlapping altitudes while capturing coverage snapshots during movement. The multi-rotor operates within the Downtown West environment, following a plotted path in XYZ coordinates. This systematic back-and-forth trajectory ensures sufficient image overlap, enabling the generation of an accurate and detailed 3D reconstruction of the environment.

![Demo Video](Demo.mp4)

## Project Structure

- `setting.json` configurates simulation parameters for AirSim.
- `src/` Contains the code for moving the multi-rotor in grid pattern.
  - `path_code.py` Script to move the multi-rotor back and forth at multiple altitudes.
  - `plot_path_xyz.py` Script to plot the multi-rotor's path in XYZ coordinates.

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
   git clone https://github.com/MohammadH-Shirvani/coverage-back-and-forth-flight
   cd coverage-back-and-forth-flight
   ```
2. Install the required Python packages:
   ```sh
   pip install matplotlib airsim time sys argparse os math
   ```
## Usage
1. Preparing the Environment
   - Place the multi-rotor:
   Open your Unreal Engine project and place the multi-rotor at the starting point in front of the building where you want the path to begin.
   - Play the Environment:
   Start the environment in Unreal Engine by clicking the "Play" button. Ensure that the AirSim plugin is active and connected.
1. Run the code:
   Navigate to the src directory and run the path code:
   ```sh
   cd src
   ```
   The script accepts the following optional command-line arguments:
   
   `--building_width`: Specifies the width of the building.
   
   `--initial_altitude`: Specifies the initial altitude of the multi-rotor flight.
   
   `--building_height`: Specifies the height of the building.

   ```sh
   python path_code.py --building_width 26 --initial_altitude 13 --building_height 12
   ```
   
3. Plot the path:
   Ensure the airsim_rec.txt file is correctly placed in the directory. The airsim_rec.txt file is used to record the multi-rotor's path during the simulation. It
   is expected to be
   located in the settings directory. This file contains the recorded multi-rotor path data required for plotting.
   ```sh
   python plot_path_xyz.py
   ```
