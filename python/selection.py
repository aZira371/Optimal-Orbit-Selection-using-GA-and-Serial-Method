"""
Parent Selection Module

Implements root-based parent selection for genetic algorithm.
"""

import numpy as np


def root_parent_select(population: np.ndarray, fitness: np.ndarray, popu_size: int) -> np.ndarray:
    """
    Select parents using inverse square root rank-based selection.
    Lower fitness (better) gets higher selection probability.
    
    Args:
        population: 2D array of population
        fitness: Array of fitness values
        popu_size: Population size
        
    Returns:
        Selected parents array
    """
    # Rank the population based on fitness (ascending order)
    sorted_indices = np.argsort(fitness)
    
    # Assign ranks inversely (lower fitness gets higher rank)
    ranks = np.arange(1, popu_size + 1)  # Lowest fitness has rank 1
    
    # Calculate selection values proportional to 1/sqrt(rank)
    raw_selection_values = 1.0 / np.sqrt(ranks)
    
    # Scale the raw selection values so that their sum equals the population size
    scaled_selection_values = raw_selection_values * (popu_size / np.sum(raw_selection_values))
    
    # Determine the number of parents each individual should produce
    expected_counts = scaled_selection_values
    
    # Initialize the selected parents matrix
    n_genes = population.shape[1]
    selected_parents = np.zeros((popu_size, n_genes), dtype=population.dtype)
    parent_index = 0
    pointer = np.random.random() * (1.0 / popu_size)  # Random start
    cumulative_sum = 0
    
    for i in range(popu_size):
        cumulative_sum = cumulative_sum + expected_counts[i]
        while pointer < cumulative_sum and parent_index < popu_size:
            # Select the corresponding individual from the population
            selected_parents[parent_index, :] = population[sorted_indices[i], :]
            parent_index += 1
            pointer += 1
    
    # Fill any remaining spots (edge case)
    while parent_index < popu_size:
        selected_parents[parent_index, :] = population[sorted_indices[0], :]
        parent_index += 1
    
    return selected_parents


if __name__ == "__main__":
    # Test parent selection
    population = np.array([
        [1, 2, 3, 4, 5],
        [1, 3, 2, 4, 5],
        [1, 4, 3, 2, 5],
        [1, 5, 4, 3, 2],
        [1, 2, 4, 3, 5]
    ])
    fitness = np.array([100, 150, 80, 200, 120])
    
    parents = root_parent_select(population, fitness, 5)
    print("Selected parents:")
    print(parents)
