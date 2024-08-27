import numpy as np
import os
import json

from scipy.integrate import quad
from scipy.stats import uniform
from scipy.stats import norm
from scipy.stats import powerlaw
from scipy.stats import rv_continuous
from scipy.stats import rv_histogram

class Mapper:
    def __init__(self, coordinate_system='cartesian'):
        self.coordinate_system = coordinate_system
        self.n_points = 1000  # Default number of points

    def set_number_of_points(self, n_points):
        """
        Set the number of random points to generate.

        Parameters:
        - n_points (int): Number of random points to generate.
        """
        self.n_points = n_points

    def generate_random_points(self, box_size):
        """
        Generate random points within a box and save each point's coordinates as a subdictionary in a JSON file.

        Parameters:
        - box_size (tuple of floats): Dimensions of the box.
            For cartesian coordinates: (box_x, box_y, box_z).
            For cylindrical coordinates: (radius, height, theta_max).
            For spherical coordinates: (radius, theta_max, phi_max)
        - output_dir (str): Directory to save the output file.
        """
        if self.coordinate_system == 'cartesian':
            points_dict = self._generate_random_points_cartesian(box_size)
        elif self.coordinate_system == 'cylindrical':
            points_dict = self._generate_random_points_cylindrical(box_size)
        elif self.coordinate_system == 'spherical':
            points_dict = self._generate_random_points_spherical(box_size)
        else:
            raise ValueError(f"Unsupported coordinate system: {self.coordinate_system}. Supported systems are 'cartesian' and 'cylindrical'.")

        return points_dict

    def _generate_random_points_cartesian(self, box_size):
        """
        Generate random points within a cartesian box and save each point's coordinates as a subdictionary in a JSON file.

        Parameters:
        - box_size (tuple of floats): Dimensions of the box in the form (box_x, box_y, box_z).
        - output_dir (str): Directory to save the output file.
        """
        box_x, box_y, box_z = box_size

        points = np.random.rand(self.n_points, 3) * np.array([box_x, box_y, box_z])

        points_dict = {
            'box_size': box_size,
            'coordinate_system': 'cartesian',
            'points': []
        }

        for i in range(self.n_points):
            point_dict = {
                'x': points[i, 0],
                'y': points[i, 1],
                'z': points[i, 2]
            }
            points_dict['points'].append(point_dict)

        return points_dict

    def _generate_random_points_cylindrical(self, box_size):
        """
        Generate random points within a cylindrical box and save each point's coordinates as a subdictionary in a JSON file.

        Parameters:
        - box_size (tuple of floats): Dimensions of the box in the form (radius, height, theta_max).
        - output_dir (str): Directory to save the output file.
        """
        radius, height, theta_max = box_size

        r_vals = radius * np.sqrt(np.random.rand(self.n_points))
        theta_vals = np.random.rand(self.n_points) * theta_max
        z_vals = np.random.rand(self.n_points) * height

        points = np.zeros((self.n_points, 3))
        points[:, 0] = r_vals * np.cos(theta_vals)
        points[:, 1] = r_vals * np.sin(theta_vals)
        points[:, 2] = z_vals

        points_dict = {
            'box_size': box_size,
            'coordinate_system': 'cylindrical',
            'points': []
        }

        for i in range(self.n_points):
            point_dict = {
                'x': points[i, 0],
                'y': points[i, 1],
                'z': points[i, 2]
            }
            points_dict['points'].append(point_dict)

        return points_dict

    def _generate_random_points_spherical(self, box_size):
        """
        Generate random points within a spherical box and save each point's coordinates as a subdictionary in a JSON file.

        Parameters:
        - box_size (tuple of floats): Dimensions of the box in the form (radius, height, theta_max).
        - output_dir (str): Directory to save the output file.
        """
        radius_max, theta_max, phi_max = box_size

        r_vals = np.sqrt(np.random.rand(self.n_points)) * radius_max
        theta_vals = np.random.uniform(-np.pi, np.pi, self.n_points)
        phi_vals = np.arccos(np.random.uniform(-np.pi, np.pi, self.n_points))

        print(r_vals[:5])
        print(phi_vals[:5])
        print(theta_vals[:5])
        print(np.random.uniform(np.cos(-np.pi), np.cos(phi_max), self.n_points))

        points = np.zeros((self.n_points, 3))   
        points[:, 0] = r_vals * np.sin(phi_vals) * np.cos(theta_vals)
        points[:, 1] = r_vals * np.sin(phi_vals) * np.sin(theta_vals)
        points[:, 2] = r_vals * np.cos(phi_vals)

        points_dict = {
            'box_size': box_size,
            'coordinate_system': 'spherical',
            'points': []
        }

        for i in range(self.n_points):
            point_dict = {
                'x': points[i, 0],
                'y': points[i, 1],
                'z': points[i, 2]
            }
            points_dict['points'].append(point_dict)

        return points_dict

    def assign_luminosity(self, points_dict, lum_func='powerlaw', **kwargs):
        """
        Generate luminosities from a given luminosity function for each simulated point.

        Parameters:
        - args:
            points_dict: array of dicts for each point
            lum_func
        - kwargs:
            For powerlaw: 'alpha': , 'lower': , 'upper': .
            For schechter: 'alpha':, 'L_star':, 'lower': , 'upper': .
            For broken powerlaw function: 'alpha_1': , 'alpha_2':, 'break': , 'lower': , 'upper': .
        """
        if lum_func == 'powerlaw':
            try:
                lum_array = self._powerlaw_generate()
            except TypeError:
                print("Must include keyword arguments for powerlaw (alpha, lower, upper)")

        elif lum_func == 'schechter':
            try:
                lum_array = self._schechter_generate(kwargs['alpha'], kwargs['L_star'], kwargs['lower'], kwargs['upper'])
            except TypeError:
                print("Must include keyword arguments for schechter function (alpha, L_star, lower, upper)")

        elif lum_func == 'uniform':
            try:
                lum_array = self._uniform_generate(kwargs['lower'], kwargs['upper'])
            except TypeError:
                print("Must include keyword arguments for schechter function (alpha, L_star, lower, upper)")

        else:
            raise ValueError("Luminosity function not supported; only 'powerlaw' and 'schechter' may be passed")
        
        for i in range(len(points_dict['points'])):
            points_dict['points'][i]['lum'] = lum_array[i]
        
        return points_dict

    def _uniform_generate(self, lower, upper):
        return np.random.uniform(lower, upper, self.n_points)
    
    def _powerlaw_generate(self, alpha, lower, upper):
        return scipy.stats.powerlaw.rvs(alpha, loc = lower, scale = upper-lower, size=self.n_points)


    def write_to_json(self, points_dict, output_dir, filename):
        """
        Write the generated points dictionary to a JSON file.

        Parameters:
        - output_dir (str): Directory to save the output file.
        - filename (str): Name of the output JSON file.
        """
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, filename)

        with open(output_filename, 'w') as json_file:
            json.dump(points_dict, json_file, indent=4)

        print(f"Saved generated points to {output_filename}")
