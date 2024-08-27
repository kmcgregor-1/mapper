"""
from mapper import Mapper
from mapper import VisualizerUtils
import matplotlib.pyplot as plt
import numpy as np

generator = Mapper(coordinate_system='cylindrical')
generator.set_number_of_points(2000)
points = generator.generate_random_points((10.0, 10.0, 2*np.pi))
print(points)
points_with_luminosities = generator.assign_luminosity(points, lum_func='uniform', alpha=-2, lower=0, upper=1)

generator.write_to_json(points_with_luminosities, './output', 'random_points_cylindrical.json')

visualizer = VisualizerUtils(population_path='./output/random_points_cylindrical.json')
pop = visualizer.get_population()

x,y,z,lum = [dict['x'] for dict in pop], [dict['y'] for dict in pop], [dict['z'] for dict in pop], [dict['lum'] for dict in pop]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(x,y,z, s = (np.array(lum))*20)
ax.scatter(0,0,5, s = 100, c='orange', marker='*')

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.set_zlim(0,10)

plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_random_spherical_points(num_points, r_range = (0,1), ra_range=(0, 2*np.pi), dec_range=(-np.pi/2, np.pi/2)):
    # Generate random distances, RA (phi), and Dec (theta)
    dist = np.sqrt(np.random.rand(num_points)) * r_range[1] # distances from the origin
    ra = np.random.uniform(ra_range[0], ra_range[1], num_points)  # right ascension (phi)
    dec = np.arcsin(np.random.uniform(np.sin(dec_range[1]), np.sin(dec_range[0]), num_points))  # declination (theta)

    print(ra[:5])
    print(dec[:5])
    print(dist[:5])

    # Convert spherical coordinates to Cartesian coordinates
    x = dist * np.cos(dec) * np.sin(ra)
    y = dist * np.sin(dec) * np.sin(ra)
    z = dist * np.cos(ra)

    return x, y, z

# Number of points to generate
num_points = 5000

# Specify ranges for ra and dec
r_range = (0,10)
ra_range = (0, np.deg2rad(360))  # Range of right ascension (phi) in radians
dec_range = (np.deg2rad(-90), np.deg2rad(90))  # Range of declination (theta) in radians

# Generate random spherical points within specified ranges
x, y, z = generate_random_spherical_points(num_points, r_range=r_range)#, ra_range=ra_range, dec_range=dec_range)

# Plotting the spherical distribution
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, marker='.', color='b')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.set_zlim(-10,10)

ax.set_title('Spherically Symmetric Distribution of Random Points')

plt.show()
