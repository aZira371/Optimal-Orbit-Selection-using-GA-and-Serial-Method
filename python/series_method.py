#!/usr/bin/env python3
"""
Series Method for Optimal Orbit Selection

Implements a greedy serial method to find an optimal order of orbit visits
for space debris removal that minimizes spent propellant mass.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

from tle_parser import tle_to_orbital_params
from orbital_mechanics import plane_change


def run_series_method():
    """Run the series method for optimal orbit selection."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tle_file = os.path.join(script_dir, '..', 'Targeted_SDs_2LE.txt')
    
    # Problem parameters
    dry_mass = 795  # Initial dry mass in kg
    propmass = 2700  # Propellant mass in kg
    sysmass = dry_mass + propmass
    sd_mass = 1500  # Space debris mass in kg
    i_sp = 300  # Specific impulse in seconds
    g_sl = 9.81  # Gravitational acceleration at Earth's surface in m/s^2
    
    # Load orbital parameters from TLE file
    orbparam = tle_to_orbital_params(tle_file)
    # orbits: [inclination, semi-major axis]
    orbits = orbparam[:21, [2, 0]]  # Take first 21 orbits
    n = orbits.shape[0]
    a = orbits[:, 1]  # Semi-major axes
    inclinations = orbits[:, 0]  # Inclinations
    sd_number = np.arange(1, n + 1)  # 1-indexed orbit numbers
    
    # Sort by semi-major axis
    sorted_indices = np.argsort(a)
    a_sorted = a[sorted_indices]
    inclinations_sorted = inclinations[sorted_indices]
    sd_number_sorted = sd_number[sorted_indices]
    
    current_orbit = 0  # 0-indexed (first in sorted list)
    visited = np.zeros(n, dtype=bool)
    visited[current_orbit] = True
    sequence = [sd_number_sorted[current_orbit]]
    total_delta_v = 0
    
    # Initialize mass tracking
    prop_mass_change = np.zeros(n)
    total_mass_change = np.zeros(n)
    prop_mass_change[0] = propmass
    total_mass_change[0] = dry_mass + propmass
    
    for i in range(n - 1):
        spent_prop_mass_o = np.inf
        delta_v_opti = np.inf
        selected_orbit = -1
        
        for j in range(n):
            if not visited[j]:
                # Calculate delta-v for the plane change
                delta_v = plane_change(inclinations_sorted[current_orbit], inclinations_sorted[j],
                                       a_sorted[current_orbit], a_sorted[j])
                
                # Calculate the propellant mass spent for this maneuver
                dry_mass_with_sd = dry_mass + sd_mass  # Add SD mass
                spent_prop_mass = (dry_mass_with_sd + propmass) * (1 - np.exp(-delta_v / (i_sp * g_sl)))
                
                # Skip invalid fuel mass
                if spent_prop_mass <= propmass and spent_prop_mass < spent_prop_mass_o:
                    spent_prop_mass_o = spent_prop_mass
                    delta_v_opti = delta_v
                    selected_orbit = j
        
        # Update data for valid answer
        if selected_orbit != -1:
            sequence.append(sd_number_sorted[selected_orbit])
            total_delta_v += delta_v_opti
            
            # Mass update
            propmass = propmass - spent_prop_mass_o
            dry_mass = dry_mass + sd_mass
            prop_mass_change[i + 1] = propmass
            total_mass_change[i + 1] = dry_mass + propmass
            
            # Visit update
            current_orbit = selected_orbit
            visited[current_orbit] = True
        else:
            # No valid solution, break
            print("No valid next orbit found. Breaking loop.")
            break
    
    print('Optimal sequence of orbit rendezvous based on original IDs:')
    print(sequence)
    print(f'Total delta-V required: {total_delta_v:.2f} m/s')
    print('Propellant mass after each rendezvous:')
    print(prop_mass_change[:len(sequence)])
    print('Total mass after each rendezvous:')
    print(total_mass_change[:len(sequence)])
    
    # Plot total mass change
    plt.figure()
    plt.plot(range(1, len(sequence) + 1), total_mass_change[:len(sequence)], 'ob')
    for idx in [0, len(sequence) - 1]:
        plt.text(idx + 1, total_mass_change[idx], f' {total_mass_change[idx]:.2f}',
                 verticalalignment='bottom', horizontalalignment='left')
    plt.xticks(range(1, n + 1), sequence + ['' for _ in range(n - len(sequence))])
    plt.xlabel('Orbit Number')
    plt.ylabel('Mass values in kg')
    plt.title(f'VARIATION OF TOTAL MASS orbit by orbit with SD Mass = {sd_mass} kg\nSERIES METHOD')
    plt.grid(True)
    
    # Plot propellant mass change
    plt.figure()
    plt.plot(range(1, len(sequence) + 1), prop_mass_change[:len(sequence)], 'or')
    for idx in [0, len(sequence) - 1]:
        plt.text(idx + 1, prop_mass_change[idx], f'{prop_mass_change[idx]:.2f}',
                 verticalalignment='bottom', horizontalalignment='right')
    plt.xticks(range(1, n + 1), sequence + ['' for _ in range(n - len(sequence))])
    plt.xlabel('Orbit Number')
    plt.ylabel('Mass values in kg')
    plt.title(f'VARIATION OF PROP MASS orbit by orbit with SD Mass = {sd_mass} kg\nSERIES METHOD')
    plt.grid(True)
    
    plt.show()
    
    return sequence, total_delta_v


if __name__ == "__main__":
    sequence, delta_v = run_series_method()
