import numpy as np
import os
import json

class VisualizerUtils:
    def __init__(self, population_path=None, projection='xy'):
        self.population_path = population_path
        self.projection = projection

        if not os.path.isfile(population_path):
            raise FileNotFoundError("Population file not found")
        
    def get_population(self):
        """
        fetches population from .json file
        """
        with open(self.population_path, 'r') as json_file:
            pop_dict = json.load(json_file)
        
        self.coordinate_system = pop_dict['coordinate_system']

        return pop_dict['points']
    
    def _cylindrial_to_cartesian(self):
        pass
    
    def _spherical_to_cartesian(self):
        pass
    


        