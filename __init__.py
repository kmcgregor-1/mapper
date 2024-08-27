# astrophysics_points_generator/__init__.py

# Import necessary classes or functions from your package
from .local import Mapper
from .visualize_utils import VisualizerUtils

# List modules that should be imported when using 'from package import *'
__all__ = [
    'Mapper'
    'VisualizerUtils'
]