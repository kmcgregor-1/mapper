

# mapper: a simple generator forrandom spatial distributions of sources

NOTE: I made this simple repository to learn how to use github for source control. Please do not take it too seriously :-)

This repository provides Python classes to generate random points in various coordinate systems and cosmological distances for astrophysics research.

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Overview

The repository includes two main classes for generating points:
- `local`: Generates random points in Cartesian, cylindrical, and spherical coordinates.
- `CosmologicalPointsGenerator`: Generates random points with cosmological distances (comoving, proper, luminosity). (*WIP*)

Points are generated and saved as JSON files, suitable for further analysis in astrophysical simulations. A test script is provided for 3d visualization

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kmcgregor-1/mapper.git
   cd mapper