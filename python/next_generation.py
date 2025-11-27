"""
Next Generation Module

Creates the next generation of population from parents and children.
"""

import numpy as np


def next_popu(prev_popu: np.ndarray, child: np.ndarray, fitness: np.ndarray) -> np.ndarray:
    """
    Create next generation by combining best half of previous population with children.
    
    Args:
        prev_popu: Previous population
        child: Offspring population
        fitness: Fitness values of previous population
        
    Returns:
        New population
    """
    popu_size = prev_popu.shape[0]
    
    # Sort based on fitness (ascending - lower is better)
    best_order_indices = np.argsort(fitness)
    
    # Take best half from previous population and half from children
    half_size = popu_size // 2
    new_popu = np.vstack([
        prev_popu[best_order_indices[:half_size], :],
        child[:half_size, :]
    ])
    
    return new_popu


def elite_next_popu(prev_popu: np.ndarray, child: np.ndarray, fitness: np.ndarray) -> np.ndarray:
    """
    Create next generation with elitism - preserving top 10% of population.
    
    Args:
        prev_popu: Previous population
        child: Offspring population
        fitness: Fitness values of previous population
        
    Returns:
        New population
    """
    popu_size = prev_popu.shape[0]
    
    # Preserve 10% of population (elites)
    preserve_count = int(np.ceil(0.1 * popu_size))
    
    # 90% population will be children
    child_count = popu_size - preserve_count
    
    # Sort based on fitness (ascending - lower is better)
    best_order_indices = np.argsort(fitness)
    
    # Allot preserve fraction to new population
    preserved_popu = prev_popu[best_order_indices[:preserve_count], :]
    
    # Rest are children
    new_popu = np.vstack([preserved_popu, child[:child_count, :]])
    
    return new_popu


if __name__ == "__main__":
    # Test next generation creation
    prev_popu = np.array([
        [3, 1, 2, 4, 5],
        [3, 5, 4, 2, 1],
        [3, 2, 5, 1, 4],
        [3, 4, 1, 5, 2]
    ])
    
    child = np.array([
        [3, 2, 1, 4, 5],
        [3, 5, 1, 2, 4],
        [3, 1, 5, 4, 2],
        [3, 4, 2, 5, 1]
    ])
    
    fitness = np.array([100, 80, 120, 90])
    
    new_pop = next_popu(prev_popu, child, fitness)
    print("Next population (regular):")
    print(new_pop)
    
    elite_pop = elite_next_popu(prev_popu, child, fitness)
    print("\nNext population (elite):")
    print(elite_pop)
