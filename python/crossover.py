"""
Crossover Module

Implements crossover operations for the genetic algorithm.
"""

import numpy as np


def ordered_crossing(parent1: np.ndarray, parent2: np.ndarray, crossover_location: int,
                     n: int, min_a_start_index: int) -> np.ndarray:
    """
    Perform ordered crossover between two parents.
    
    Args:
        parent1: First parent chromosome
        parent2: Second parent chromosome
        crossover_location: Position for crossover (1-indexed)
        n: Number of genes
        min_a_start_index: Fixed starting orbit index
        
    Returns:
        Child chromosome
    """
    # Initialize the child with zeros
    child = np.zeros(n, dtype=int)
    
    # Set the first index to the fixed start orbit
    child[0] = min_a_start_index
    
    # Create segments from the selected parents
    # Note: MATLAB is 1-indexed, Python is 0-indexed
    segment = parent1[1:crossover_location]
    
    # Get remaining elements from parent2 that are not in segment
    remaining = [x for x in parent2[1:] if x not in segment]
    
    # Create the child sequence
    child[1:crossover_location] = segment
    
    # Fill the remaining slots in the child with the 'remaining' sequence
    remaining_slots = n - crossover_location
    child[crossover_location:] = remaining[:remaining_slots]
    
    return child


def crossover(parents: np.ndarray, popu_size: int, crossover_rate: float,
              min_a_start_index: int) -> np.ndarray:
    """
    Apply crossover to create offspring.
    
    Args:
        parents: 2D array of parent chromosomes
        popu_size: Population size
        crossover_rate: Probability of crossover
        min_a_start_index: Fixed starting orbit index
        
    Returns:
        2D array of offspring
    """
    num_parents, n = parents.shape
    child = np.zeros((popu_size, n), dtype=int)
    
    i = 0
    while i < popu_size:
        if np.random.random() < crossover_rate:
            parent1 = parents[np.random.randint(num_parents), :]
            parent2 = parents[np.random.randint(num_parents), :]
            crossover_location = np.random.randint(2, n + 1)  # Start from index 2 (1-indexed)
            
            # Ordered crossover
            child[i, :] = ordered_crossing(parent1, parent2, crossover_location, n, min_a_start_index)
            if i + 1 < popu_size:
                child[i + 1, :] = ordered_crossing(parent2, parent1, crossover_location, n, min_a_start_index)
            i += 2
        else:
            child[i, :] = parents[np.random.randint(num_parents), :]
            if i + 1 < popu_size:
                child[i + 1, :] = parents[np.random.randint(num_parents), :]
            i += 2
    
    return child


if __name__ == "__main__":
    # Test crossover
    parents = np.array([
        [3, 1, 2, 4, 5],
        [3, 5, 4, 2, 1],
        [3, 2, 5, 1, 4],
        [3, 4, 1, 5, 2]
    ])
    
    children = crossover(parents, 4, 0.9, 3)
    print("Children after crossover:")
    print(children)
