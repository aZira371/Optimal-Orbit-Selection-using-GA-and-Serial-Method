"""
Fitness Evaluation Module

Evaluates fitness of population members based on spent propellant mass.
"""

import numpy as np
from objective import obj_min_spent_prop_mass


def fitness_evaluate(population: np.ndarray, orbits: np.ndarray, dry_mass_0: float,
                     prop_mass_0: float, isp: float, g_0: float, sd_mass: float) -> np.ndarray:
    """
    Evaluate fitness for entire population.
    
    Args:
        population: 2D array where each row is an individual (orbit order)
        orbits: Array of orbit parameters [inclination, semi-major axis]
        dry_mass_0: Initial dry mass in kg
        prop_mass_0: Initial propellant mass in kg
        isp: Specific impulse in seconds
        g_0: Gravitational acceleration at Earth's surface in m/s^2
        sd_mass: Space debris mass in kg
        
    Returns:
        Array of fitness values (spent propellant mass) for each individual
    """
    popu_size = population.shape[0]
    fitness = np.zeros(popu_size)
    
    for i in range(popu_size):
        order = population[i, :]
        spent_prop_mass_total = obj_min_spent_prop_mass(order, orbits, dry_mass_0,
                                                        prop_mass_0, isp, g_0, sd_mass, False)
        fitness[i] = spent_prop_mass_total
    
    return fitness


if __name__ == "__main__":
    # Test fitness evaluation
    orbits = np.array([
        [82.5, 6800],
        [82.0, 6900],
        [83.0, 7000],
        [81.5, 6750],
        [82.2, 6850]
    ])
    
    population = np.array([
        [1, 2, 3, 4, 5],
        [1, 3, 2, 4, 5],
        [1, 4, 3, 2, 5]
    ])
    
    fitness = fitness_evaluate(population, orbits, 795, 2700, 300, 9.81, 0)
    print(f"Fitness values: {fitness}")
