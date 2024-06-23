import matplotlib.pyplot as plt

# Initialize lists to hold the data from each column
pos_x = []
pos_y = []
pos_z = []

# Open your text file
with open("airsim_rec.txt", "r") as file:
    # Read the first line to get the headers
    headers = file.readline().strip().split()
    
    # Determine the index of each position variable
    idx_x = headers.index('POS_X')
    idx_y = headers.index('POS_Y')
    idx_z = headers.index('POS_Z')
    
    # Read each subsequent line
    for line in file:
        # Split the line into components based on spaces or tabs
        parts = line.strip().split()
        
        # Append the correct part using the index found above
        pos_x.append(float(parts[idx_x]))
        pos_y.append(float(parts[idx_y]))
        pos_z.append(-float(parts[idx_z]))

# Create a new figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the trajectory
ax.plot(pos_x, pos_y, pos_z, marker='o', linestyle='-', color='purple', label='Drone trajectory', linewidth=0.1)

# Set labels and title
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Z Position')
ax.set_title('3D Trajectory of Drone Flight')

# Add a legend
ax.legend()

# Display the plot
plt.show()

# plt.savefig('drone_trajectory.png')