import airsim
import time
import os
import math

# Camera Specific
IMAGE_HEIGHT = 1280   # Same as the image height in setting.json
IMAGE_WIDTH = 2560    # Same as the image width in setting.json
CAMERA_FOV_HORIZONTAL = 90  # Horizontal field of view of the camera in degrees

# Vertical FoV Calculation
aspect_ratio = IMAGE_WIDTH / IMAGE_HEIGHT
horizontal_fov_rad = math.radians(CAMERA_FOV_HORIZONTAL)
vertical_fov_rad = 2 * math.atan(math.tan(horizontal_fov_rad/2) / aspect_ratio)     # Vertical FoV
CAMERA_FOV_VERTICAL = math.degrees(vertical_fov_rad)    # Vertical field of view

# Overlap definition
lateral_overlap = 0.8
longtitudal_overlap = 0.9

# Start number of image index
index = 0

class position:
    def __init__(self, pos):
        self.x = pos.x_val
        self.y = pos.y_val
        self.z = pos.z_val

# Make the drone fly in a grid
class DroneFlight:
    def __init__(self, building_width = 26, initial_altitude=11, building_height=12):
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
        Fly the drone along the building's width at a given altitude and capture images with the specified horizontal overlap.
        """
        self.current_position = self.client.getMultirotorState().kinematics_estimated.position
        z = -altitude
        self.client.moveToPositionAsync(self.current_position.x_val, self.current_position.y_val, z, 2).join()
        while abs(self.current_position.y_val - self.start.y_val) <= self.building_width:
            # Capture image
            self.take_snapshot()
            # Move to next position
            self.current_position.y_val += direction * self.interval
            print('Y val of Current position : ', self.current_position.y_val)
            self.client.moveToPositionAsync(self.current_position.x_val, self.current_position.y_val, z, 2).join()
        
        # Update start position of path after completing the flight along building width
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
        print("Initial Distance:", self.distance_data)

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
        while self.current_altitude >= vertical_coverage/4:
            # Fly from start to end
            self.fly_and_capture(self.current_altitude, 1)
            # Decrease the altitude
            self.current_altitude *= lateral_overlap
            # Fly back from end to start
            self.fly_and_capture(self.current_altitude, -1)
            self.current_altitude *= lateral_overlap

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

    flight = DroneFlight()
    # Perform the flights
    flight.perform_flights()