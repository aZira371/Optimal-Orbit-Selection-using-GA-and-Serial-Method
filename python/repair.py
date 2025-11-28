"""
Repair Module

Repairs invalid solutions to make them feasible.
"""

import numpy as np
from validity import check_validity


def repair(order: np.ndarray, orbits: np.ndarray, dry_mass_0: float,
           prop_mass_0: float, isp: float, g_0: float, sd_mass: float) -> np.ndarray:
    """
    Repair an invalid orbit order to make it feasible.
    
    Args:
        order: Array of orbit indices in visitation order
        orbits: Array of orbit parameters
        dry_mass_0: Initial dry mass in kg
        prop_mass_0: Initial propellant mass in kg
        isp: Specific impulse in seconds
        g_0: Gravitational acceleration
        sd_mass: Space debris mass in kg
        
    Returns:
        Repaired order array
    """
    repaired_order = order.copy()
    max_attempts = 100  # Maximum number of attempts before restarting
    attempt_count = 0
    n = len(order)
    
    while True:
        if check_validity(repaired_order, orbits, dry_mass_0, prop_mass_0, isp, g_0, sd_mass):
            break
        
        # Increase attempt count
        attempt_count += 1
        
        # If too many attempts, restart with a new random order
        if attempt_count > max_attempts:
            # Keep the first element fixed, randomize the rest
            rest = np.random.permutation(np.arange(1, n)) + 1
            repaired_order = np.concatenate([[repaired_order[0]], rest])
            attempt_count = 0
            continue
        
        # Choose a modification type: reverse or shuffle a subsequence
        modification_type = np.random.randint(1, 3)
        
        # Define the indices for the subsequence, excluding the first index
        start_idx = np.random.randint(1, n)  # Random start index between 1 and N-1
        max_length = n - start_idx  # Maximum length of subsequence
        
        # Ensure valid subsequence length
        if max_length >= 2:
            length_subseq = np.random.randint(2, max_length + 1)  # Length of subsequence between 2 and max_length
            end_idx = start_idx + length_subseq
            
            # Ensure end_idx does not exceed the length of the order
            end_idx = min(end_idx, n)
            
            if modification_type == 1:
                # Reverse a random subsequence
                repaired_order[start_idx:end_idx] = repaired_order[start_idx:end_idx][::-1]
            else:
                # Shuffle a random subsequence
                subsequence = repaired_order[start_idx:end_idx].copy()
                np.random.shuffle(subsequence)
                repaired_order[start_idx:end_idx] = subsequence
    
    return repaired_order


if __name__ == "__main__":
    # Test repair function
    orbits = np.array([
        [82.5, 6800],
        [82.0, 6900],
        [83.0, 7000],
        [81.5, 6750],
        [82.2, 6850]
    ])
    
    order = np.array([1, 5, 4, 3, 2])
    print(f"Original order: {order}")
    
    repaired = repair(order, orbits, 795, 2700, 300, 9.81, 0)
    print(f"Repaired order: {repaired}")
