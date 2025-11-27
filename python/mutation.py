"""
Mutation Module

Implements various mutation operations for the genetic algorithm.
"""

import numpy as np


def mutation(child: np.ndarray, mutate_rate: float, min_a_start_index: int) -> np.ndarray:
    """
    Apply swap mutation to offspring.
    Randomly swaps two genes (excluding the fixed starting position).
    
    Args:
        child: 2D array of offspring chromosomes
        mutate_rate: Probability of mutation
        min_a_start_index: Fixed starting orbit index (not used directly, but position 0 is protected)
        
    Returns:
        Mutated offspring
    """
    popu_size, n = child.shape
    
    for i in range(popu_size):
        if np.random.random() < mutate_rate:
            # Select two random indices to swap (excluding first position)
            indices = np.random.choice(range(1, n), 2, replace=False)
            
            # Swap the elements
            child[i, indices[0]], child[i, indices[1]] = child[i, indices[1]], child[i, indices[0]]
    
    return child


def inverse_mutation(child: np.ndarray, mutate_rate: float, min_a_start_index: int) -> np.ndarray:
    """
    Apply inverse mutation to offspring.
    Reverses a random subsequence of genes (excluding the fixed starting position).
    
    Args:
        child: 2D array of offspring chromosomes
        mutate_rate: Probability of mutation
        min_a_start_index: Fixed starting orbit index
        
    Returns:
        Mutated offspring
    """
    popu_size, n = child.shape
    
    for i in range(popu_size):
        if np.random.random() < mutate_rate:
            # Select a random subset of genes to invert
            # Maximum subset length is n-1 (to ensure at least 2 genes and start from index 1)
            max_subset_length = min(n - 1, n - 1)  # Leave room for start position
            if max_subset_length < 2:
                continue  # Skip if array is too small
            subset_length = np.random.randint(2, max_subset_length + 1)  # Minimum 2 genes
            max_start = n - subset_length
            if max_start < 1:
                continue  # Skip if not enough room
            subset_start = np.random.randint(1, max_start + 1)  # Start from index 1
            
            # Define the subset indices
            subset_end = subset_start + subset_length
            
            # Invert the selected subset
            child[i, subset_start:subset_end] = child[i, subset_start:subset_end][::-1]
    
    return child


def scram_mutation(child: np.ndarray, mutate_rate: float, min_a_start_index: int) -> np.ndarray:
    """
    Apply scramble mutation to offspring.
    Randomly shuffles a subsequence of genes (excluding the fixed starting position).
    
    Args:
        child: 2D array of offspring chromosomes
        mutate_rate: Probability of mutation
        min_a_start_index: Fixed starting orbit index
        
    Returns:
        Mutated offspring
    """
    popu_size, n = child.shape
    
    for i in range(popu_size):
        if np.random.random() < mutate_rate:
            # Select a random subset of genes to scramble
            # Maximum subset length is n-1 (to ensure at least 2 genes and start from index 1)
            max_subset_length = min(n - 1, n - 1)  # Leave room for start position
            if max_subset_length < 2:
                continue  # Skip if array is too small
            subset_length = np.random.randint(2, max_subset_length + 1)  # Minimum 2 genes
            max_start = n - subset_length
            if max_start < 1:
                continue  # Skip if not enough room
            subset_start = np.random.randint(1, max_start + 1)  # Start from index 1
            
            # Define the subset indices
            subset_end = subset_start + subset_length
            
            # Scramble the selected subset
            subset = child[i, subset_start:subset_end].copy()
            np.random.shuffle(subset)
            child[i, subset_start:subset_end] = subset
    
    return child


if __name__ == "__main__":
    # Test mutations
    child = np.array([
        [3, 1, 2, 4, 5],
        [3, 5, 4, 2, 1],
        [3, 2, 5, 1, 4],
        [3, 4, 1, 5, 2]
    ])
    
    print("Original:")
    print(child)
    
    mutated = mutation(child.copy(), 1.0, 3)
    print("\nAfter swap mutation:")
    print(mutated)
    
    inverse_mutated = inverse_mutation(child.copy(), 1.0, 3)
    print("\nAfter inverse mutation:")
    print(inverse_mutated)
    
    scram_mutated = scram_mutation(child.copy(), 1.0, 3)
    print("\nAfter scramble mutation:")
    print(scram_mutated)
