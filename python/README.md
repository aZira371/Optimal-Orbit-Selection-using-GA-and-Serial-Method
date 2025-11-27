# Optimal Orbit Selection - Python Version

This directory contains the Python implementation of the Optimal Orbit Selection project using Genetic Algorithm and Serial Method for space debris removal mission planning.

## Overview

The project implements three optimization methods to find the optimal order of orbit visits for a spacecraft performing space debris removal:

1. **Genetic Algorithm (GA)** - A metaheuristic approach using evolution-inspired operators
2. **Series Method** - A greedy algorithm that selects the best next orbit at each step
3. **Brute Force Permutation** - Exhaustive search for small problem sizes

## Requirements

- Python 3.7+
- NumPy >= 1.20.0
- Matplotlib >= 3.3.0

Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
python/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── ga_main.py               # Main Genetic Algorithm implementation
├── series_method.py         # Greedy serial method
├── brute_force.py           # Exhaustive permutation search
├── tle_parser.py            # TLE file parser
├── orbital_mechanics.py     # Delta-V calculation functions
├── objective.py             # Objective function (spent propellant mass)
├── fitness.py               # Fitness evaluation for GA
├── population.py            # Population initialization
├── selection.py             # Parent selection (root-based)
├── crossover.py             # Ordered crossover operators
├── mutation.py              # Mutation operators (swap, inverse, scramble)
├── next_generation.py       # Next generation creation
├── repair.py                # Solution repair for invalid individuals
└── validity.py              # Solution validity checking
```

## Usage

### Genetic Algorithm

Run the main GA optimization:
```bash
cd python
python ga_main.py
```

This will:
- Load orbital parameters from the TLE file
- Run a genetic algorithm with configurable parameters
- Display real-time fitness evolution plots
- Output the optimal orbit visitation order and total spent propellant mass

### Series Method

Run the greedy serial method:
```bash
python series_method.py
```

### Brute Force (for small problems)

Run exhaustive search on 5 orbits:
```bash
python brute_force.py
```

## Configuration

Key parameters can be modified in the main files:

### Spacecraft Parameters
- `dry_mass_0`: Initial dry mass (kg) - default: 795
- `prop_mass_0`: Propellant mass (kg) - default: 2700
- `sd_mass`: Space debris mass per pickup (kg) - default: 1500
- `isp`: Specific impulse (s) - default: 300
- `g_0`: Gravitational acceleration (m/s²) - default: 9.81

### GA Parameters
- `popu_size`: Population size - default: 500
- `max_generations`: Number of generations - default: 250
- `mutate_rate`: Mutation probability - default: 0.9
- `crossover_rate`: Crossover probability - default: 0.9

## Algorithm Details

### Genetic Algorithm Features
- **Ordered Crossover**: Preserves relative order of genes to maintain valid permutations
- **Adaptive Mutation**: Switches between swap and inverse mutation based on stagnation
- **Root-based Selection**: Uses 1/√rank selection probability
- **Elitism**: Preserves best solutions across generations
- **Repair Function**: Fixes invalid solutions that exceed propellant budget

### Objective Function
Minimizes total spent propellant mass using the Tsiolkovsky rocket equation:
```
Δm = m₀(1 - exp(-Δv/(Isp·g₀)))
```

### Delta-V Calculation
Combined plane change and altitude change maneuver:
```
Δv = √(v₁² + v₂² - 2v₁v₂cos(Δi))
```

## Data Format

The TLE (Two-Line Element) file contains orbital data in standard format. The parser extracts:
- Semi-major axis (calculated from mean motion)
- Eccentricity
- Inclination
- RAAN (Right Ascension of Ascending Node)
- Argument of Perigee
- Mean Anomaly

## Output

The algorithms produce:
1. Optimal orbit visitation sequence
2. Total spent propellant mass
3. Plots showing:
   - Fitness evolution over generations (GA only)
   - Propellant mass remaining at each step
   - Total spacecraft mass at each step
   - Population diversity (GA only)

## Comparison with MATLAB Version

This Python implementation is a direct port of the original MATLAB code with the following differences:
- Uses 0-indexed arrays internally but maintains 1-indexed orbit numbering for output
- Uses NumPy for numerical operations
- Uses Matplotlib for visualization
- Object-oriented module structure for better code organization

## License

See the main repository LICENSE file.
