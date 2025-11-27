"""
Population Initialization Module

Creates initial populations for the genetic algorithm.
"""

import numpy as np
from validity import check_validity


def popu_initialize(popu_size: int, n: int, min_a_start_index: int,
                    orbits: np.ndarray = None, dry_mass_0: float = None,
                    prop_mass_0: float = None, isp: float = None,
                    g_0: float = None, sd_mass: float = None) -> np.ndarray:
    """
    Initialize population with random permutations starting from fixed orbit.
    
    Args:
        popu_size: Number of individuals in population
        n: Number of orbits
        min_a_start_index: Index of starting orbit (1-indexed)
        orbits: Orbit parameters (optional, used for validation)
        dry_mass_0: Initial dry mass (optional)
        prop_mass_0: Initial propellant mass (optional)
        isp: Specific impulse (optional)
        g_0: Gravitational acceleration (optional)
        sd_mass: Space debris mass (optional)
        
    Returns:
        2D array of population (popu_size x n)
    """
    population = np.zeros((popu_size, n), dtype=int)
    
    for i in range(popu_size):
        # Generate remaining indices excluding the fixed starting index
        remaining_indices = [j for j in range(1, n + 1) if j != min_a_start_index]
        np.random.shuffle(remaining_indices)
        perm_order = [min_a_start_index] + remaining_indices
        population[i, :] = perm_order
    
    return population


def popu_initialize_valid(popu_size: int, n: int, min_a_start_index: int,
                          orbits: np.ndarray, dry_mass_0: float,
                          prop_mass_0: float, isp: float,
                          g_0: float, sd_mass: float) -> np.ndarray:
    """
    Initialize population with valid random permutations starting from fixed orbit.
    Only includes individuals that pass validity check.
    
    Args:
        popu_size: Number of individuals in population
        n: Number of orbits
        min_a_start_index: Index of starting orbit (1-indexed)
        orbits: Orbit parameters
        dry_mass_0: Initial dry mass
        prop_mass_0: Initial propellant mass
        isp: Specific impulse
        g_0: Gravitational acceleration
        sd_mass: Space debris mass
        
    Returns:
        2D array of valid population (popu_size x n)
    """
    population = np.zeros((popu_size, n), dtype=int)
    
    for i in range(popu_size):
        validity = False
        while not validity:
            # Generate remaining indices excluding the fixed starting index
            remaining_indices = [j for j in range(1, n + 1) if j != min_a_start_index]
            np.random.shuffle(remaining_indices)
            perm_order = np.array([min_a_start_index] + remaining_indices)
            
            if check_validity(perm_order, orbits, dry_mass_0, prop_mass_0, isp, g_0, sd_mass):
                population[i, :] = perm_order
                validity = True
    
    return population


if __name__ == "__main__":
    # Test population initialization
    pop = popu_initialize(5, 10, 3)
    print("Random population (5 individuals, 10 orbits, starting at orbit 3):")
    print(pop)
