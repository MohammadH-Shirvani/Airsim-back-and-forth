import airsim
import time
import sys
import argparse
import os
import math

# Camera Specifics
IMAGE_HEIGHT = 1280   # Same as the height in setting.json
IMAGE_WIDTH = 2560    # Same as the width in setting.json
CAMERA_FOV_HORIZONTAL = 90  # Horizontal field of view of the camera in degrees from setting.json

# Vertical FoV Calculation
aspect_ratio = IMAGE_WIDTH / IMAGE_HEIGHT
horizontal_fov_rad = math.radians(CAMERA_FOV_HORIZONTAL)
vertical_fov_rad = 2 * math.atan(math.tan(horizontal_fov_rad/2) / aspect_ratio)
CAMERA_FOV_VERTICAL = math.degrees(vertical_fov_rad)    # Vertical FoV

# Region of interest defined as (x1, y1, x2, y2)
roi = (IMAGE_WIDTH // 3, 0, IMAGE_WIDTH * 2 // 3, IMAGE_HEIGHT)

# Overlap definition
lateral_overlap = 0.6
longtitudal_overlap = 0.8

index = 0   # First photo index

class position:
    def __init__(self, pos):
        self.x = pos.x_val
        self.y = pos.y_val
        self.z = pos.z_val

# Make the drone fly in a grid
class DroneFlight:
    def __init__(self, building_width = 26, initial_altitude=13, building_height=12):
        self.building_width = building_width
        self.initial_altitude = initial_altitude
        self.building_height = building_height
        self.snapshot_index = index

        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def calculate_interval(self, distance_to_wall):
        """
        Calculate the time interval between capturing images based on the drone's distance to the wall.
        """
        # Calculate the ground distance covered by the camera field of view
        ground_distance = 2 * distance_to_wall * math.tan(math.radians(CAMERA_FOV_HORIZONTAL / 2))
        # Calculate the interval distance considering the overlap percentage
        interval_distance = ground_distance * (1 - longtitudal_overlap)
        print('Interval distance : ', interval_distance)
        return interval_distance

    def fly_and_capture(self, altitude, direction):
        """
        Fly the drone along the building's width at a given altitude and capture images with the specified overlap.
        """
        self.current_position = self.client.getMultirotorState().kinematics_estimated.position
        z = -altitude
        self.client.moveToPositionAsync(self.current_position.x_val, self.current_position.y_val, z, 2).join()
        print(f'Current position = {self.current_position}\n Start position = {self.start} and \n Direction: {direction}')
        while abs(self.current_position.y_val - self.start.y_val) <= self.building_width:
            
            # Capture image
            self.take_snapshot()
            # Move to next position
            self.current_position.y_val += direction * self.interval
            print('Y val of Current position after interval = ', self.current_position.y_val)
            self.client.moveToPositionAsync(self.current_position.x_val, self.current_position.y_val, z, 2).join()
        self.start = self.client.getMultirotorState().kinematics_estimated.position

    def perform_flights(self):
        """
        Perform flights at multiple altitudes starting from the initial altitude.
        """
        print("arming the drone...")
        self.client.armDisarm(True)
        print("taking off...")
        self.client.takeoffAsync().join()
        
        # get distance to wall
        self.distance_data = self.client.getDistanceSensorData(vehicle_name="MyDrone").distance
        print("Distance:", self.distance_data)

        # Move to start position
        self.start = self.client.getMultirotorState().kinematics_estimated.position
        z= -self.initial_altitude
        print("climbing to position: {},{},{}".format(self.start.x_val, self.start.y_val, z))
        self.client.moveToPositionAsync(self.start.x_val, self.start.y_val, z, 2).join()

        # Calculate interval
        self.interval = self.calculate_interval(self.distance_data)
        if self.interval <= 0:
            print("Invalid interval")

        self.current_altitude = self.initial_altitude
        vertical_coverage = self.calculate_vertical_coverage()
        self.take_snapshot()
        print('Current altitude : ', self.current_altitude)
        while True:
            # Fly from left to right
            self.fly_and_capture(self.current_altitude, 1)
            # Decrease the altitude
            self.current_altitude *= lateral_overlap
            # Fly back in new decreased altitude
            self.fly_and_capture(self.current_altitude, -1)
            self.current_altitude *= lateral_overlap
            if self.current_altitude >= vertical_coverage/2:
                self.fly_and_capture(self.current_altitude, -1)
                break

        # Disable API control and disarm
        print("descending")
        self.client.moveToPositionAsync(0, 0, 0, 2).join()
        print("disarming.")
        self.client.armDisarm(False)
        self.client.enableApiControl(False)
        

    def calculate_vertical_coverage(self):
        """
        Calculate the vertical coverage of the camera based on the vertical field of view and distance data.
        """
        # Calculate the vertical coverage of the camera at the initial altitude
        vertical_coverage = 2 * self.distance_data * math.tan(math.radians(CAMERA_FOV_VERTICAL / 2))
        print('Vertical Coverage = ',vertical_coverage)
        return vertical_coverage
    
    def take_snapshot(self):
        
        # first hold our current position so drone doesn't try and keep flying while we take the picture.
        self.client.hoverAsync().join()
        print("Drone hovering...")
        time.sleep(2)

        # scene vision image in png format
        responses = self.client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Scene)])
        response = responses[0]
        filename = "photo_" + str(self.snapshot_index)
        self.snapshot_index += 1
        image_path = os.path.normpath(filename + '.png')
        airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)        
        print("Saved snapshot: {}".format(filename))
        return image_path
    
if __name__ == "__main__":

    args = sys.argv
    args.pop(0)
    arg_parser = argparse.ArgumentParser("Orbit.py makes drone fly in a circle with camera pointed at the given center vector")
    arg_parser.add_argument("--building_width", type=float, help="width of the building", default=26)
    arg_parser.add_argument("--initial_altitude", type=float, help="initial altitude of flight (in positive meters)", default=13)
    arg_parser.add_argument("--building_height", type=float, help="height of the building", default=12)
    args = arg_parser.parse_args(args)    
    flight = DroneFlight(args.building_width, args.initial_altitude, args.building_height)
    # Perform the flights
    flight.perform_flights()
