#!/usr/bin/env python3
"""
Brute Force Permutation Method for Optimal Orbit Selection

Exhaustively evaluates all permutations of orbit visits to find the optimal order.
This is only practical for small numbers of orbits (e.g., 5 orbits = 24 permutations).
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import os

from tle_parser import tle_to_orbital_params
from orbital_mechanics import plane_change


def run_brute_force():
    """Run brute force permutation to find optimal orbit order."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tle_file = os.path.join(script_dir, '..', 'Targeted_SDs_2LE.txt')
    
    # Problem parameters
    dry_mass_0 = 795  # Initial dry mass in kg
    prop_mass_0 = 2700  # Propellant mass in kg
    sd_mass = 0  # Space debris mass in kg, 45.3 for PM and 1486.542 for RB
    isp = 300  # Specific impulse in seconds
    g_0 = 9.81  # Gravitational acceleration at Earth's surface in m/s^2
    
    # Load orbital parameters from TLE file
    orbparam = tle_to_orbital_params(tle_file)
    # orbits: [inclination, semi-major axis]
    orbits = orbparam[:5, [2, 0]]  # Take first 5 orbits
    n = orbits.shape[0]
    mu = 398600
    
    # Determine the starting orbit
    # Find the index of the orbit with the minimum semi-major axis
    min_a_index = np.argmin(orbits[:, 1])
    
    # Check if all semi-major axes are equal
    if np.all(orbits[:, 1] == orbits[min_a_index, 1]):
        # If all semi-major axes are equal, choose the orbit with the minimum inclination
        start_index = np.argmin(orbits[:, 0])
    else:
        start_index = min_a_index
    
    # Generate all possible permutations of visiting the remaining orbits
    to_visit = [i for i in range(n) if i != start_index]
    all_permutations = list(permutations(to_visit))
    num_perms = len(all_permutations)
    
    # Initialize tracking arrays
    stp_mass = np.zeros((num_perms, n))
    total_mass_change = np.zeros((num_perms, n))
    prop_mass_change = np.zeros((num_perms, n))
    dry_mass_fraction = np.zeros((num_perms, n))
    prop_mass_fraction = np.zeros((num_perms, n))
    final_array = np.zeros((num_perms, n + 1))
    optimal_perm = None
    min_stp = np.inf
    
    for i, perm in enumerate(all_permutations):
        test_perm = [start_index] + list(perm)
        
        # Calculate the total delta-v for the current permutation
        total_delta_v = 0
        spent_prop_mass_total = 0
        dry_mass = dry_mass_0
        prop_mass = prop_mass_0
        
        for j in range(1, n):
            # Indices of the orbits in the permutation
            orbit1 = test_perm[j - 1]
            orbit2 = test_perm[j]
            
            inc1 = orbits[orbit1, 0]
            inc2 = orbits[orbit2, 0]
            a1 = orbits[orbit1, 1]
            a2 = orbits[orbit2, 1]
            
            # Add SD mass
            dry_mass = dry_mass + sd_mass
            
            # Plane change delta-v
            delta_v = plane_change(inc1, inc2, a1, a2)
            
            # Total delta-v
            total_delta_v += delta_v
            
            # Rocket equation
            spent_prop_mass = (dry_mass + prop_mass) * (1 - np.exp(-delta_v / (isp * g_0)))
            spent_prop_mass_total += spent_prop_mass
            prop_mass = prop_mass - spent_prop_mass  # Update prop mass after burn
            
            stp_mass[i, j] = spent_prop_mass_total
            total_mass_change[i, j] = dry_mass + prop_mass
            prop_mass_change[i, j] = prop_mass
            dry_mass_fraction[i, j] = dry_mass / (dry_mass + prop_mass)
            prop_mass_fraction[i, j] = prop_mass / (dry_mass + prop_mass)
        
        # Initial values
        dry_mass_fraction[i, 0] = dry_mass_0 / (dry_mass_0 + sd_mass + prop_mass_0)
        prop_mass_fraction[i, 0] = prop_mass_0 / (dry_mass_0 + sd_mass + prop_mass_0)
        total_mass_change[i, 0] = dry_mass_0 + sd_mass + prop_mass_0
        prop_mass_change[i, 0] = prop_mass_0
        
        # Store final array (convert to 1-indexed for display)
        final_array[i, 0] = start_index + 1
        for j in range(1, n):
            final_array[i, j] = test_perm[j] + 1
        final_array[i, n] = stp_mass[i, n - 1]
        
        if spent_prop_mass_total < min_stp:
            min_stp = spent_prop_mass_total
            optimal_perm = [x + 1 for x in test_perm]  # Convert to 1-indexed
        
        if spent_prop_mass_total > prop_mass_0:
            print('Propellant mass spent is more than carried')
            return
    
    final_index = np.argmin(final_array[:, n])
    
    print('Minimum Propellant Mass Spent:')
    print(f'{min_stp:.2f} kg')
    
    print('\nBest Permutation (Orbit Order):')
    print(optimal_perm)
    
    print('\nCorresponding Inclinations and Semi-Major Axes:')
    for idx in [x - 1 for x in optimal_perm]:  # Convert back to 0-indexed
        print(f'  Orbit {idx + 1}: inc={orbits[idx, 0]:.4f}°, a={orbits[idx, 1]:.2f} km')
    
    # Plot propellant mass change
    plt.figure()
    plt.plot(range(1, n + 1), prop_mass_change[final_index, :], 'or')
    for idx in [0, n - 1]:
        plt.text(idx + 1, prop_mass_change[final_index, idx], 
                 f'{prop_mass_change[final_index, idx]:.2f}',
                 verticalalignment='bottom', horizontalalignment='right')
    plt.xticks(range(1, n + 1), optimal_perm)
    plt.xlabel('Orbit Number')
    plt.ylabel('Mass values in kg')
    plt.legend(['Propellant Mass'])
    plt.title(f'VARIATION OF PROP MASS with SD Mass = {sd_mass} Kg\nBRUTE FORCE PERMUTATION')
    plt.ylim([np.min(prop_mass_change[final_index, :]) - 150, 
              np.max(prop_mass_change[final_index, :]) + 200])
    plt.grid(True)
    
    # Plot total mass change
    plt.figure()
    plt.plot(range(1, n + 1), total_mass_change[final_index, :], 'ob')
    for idx in [0, n - 1]:
        plt.text(idx + 1, total_mass_change[final_index, idx], 
                 f' {total_mass_change[final_index, idx]:.2f}',
                 verticalalignment='bottom', horizontalalignment='left')
    plt.xticks(range(1, n + 1), optimal_perm)
    plt.xlabel('Orbit Number')
    plt.ylabel('Mass values in kg')
    plt.legend(['Total Mass'])
    plt.title(f'VARIATION OF TOTAL MASS with SD Mass = {sd_mass} Kg\nBRUTE FORCE PERMUTATION')
    plt.ylim([np.min(total_mass_change[final_index, :]) - 100, 
              np.max(total_mass_change[final_index, :]) + 400])
    plt.grid(True)
    
    plt.show()
    
    return optimal_perm, min_stp


if __name__ == "__main__":
    optimal_order, min_spent = run_brute_force()
