#!/usr/bin/env python3
"""
Genetic Algorithm for Optimal Orbit Selection

Main file implementing a custom genetic algorithm to find the optimal order
of orbit visits for space debris removal that minimizes spent propellant mass.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

from tle_parser import tle_to_orbital_params
from population import popu_initialize
from fitness import fitness_evaluate
from repair import repair
from selection import root_parent_select
from crossover import crossover
from mutation import mutation, inverse_mutation
from next_generation import next_popu
from objective import obj_min_spent_prop_mass


def run_ga():
    """Run the genetic algorithm for optimal orbit selection."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tle_file = os.path.join(script_dir, '..', 'Targeted_SDs_2LE.txt')
    
    # Problem parameters
    dry_mass_0 = 795  # Initial dry mass in kg
    prop_mass_0 = 2700  # Propellant mass in kg
    sd_mass = 1500  # Space debris mass in kg, 0 or no SD, 50 for PM and 1500 for RB
    isp = 300  # Specific impulse in seconds
    g_0 = 9.81  # Gravitational acceleration at Earth's surface in m/s^2
    
    # Load orbital parameters from TLE file
    orbparam = tle_to_orbital_params(tle_file)
    # orbits: [inclination, semi-major axis]
    orbits = orbparam[:20, [2, 0]]  # Take first 20 orbits, columns: inclination, semi-major axis
    n = orbits.shape[0]
    
    # Find starting orbit (minimum semi-major axis)
    min_a_ind = np.argmin(orbits[:, 1]) + 1  # 1-indexed
    min_a_start_index = min_a_ind
    
    # GA settings
    popu_size = 500  # Population size
    max_generations = 250  # Number of generations
    mutate_rate = 0.9  # Mutation rate
    crossover_rate = 0.9  # Crossover rate
    mean_fitness = np.zeros(max_generations)
    best_fitness = np.zeros(max_generations)
    
    # Live plot of fitness values
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel('Generation number')
    ax.set_ylabel('Fitness values')
    ax.set_title(f'VARIATION OF FITNESS GENERATION BY GENERATION with SD Mass = {sd_mass} Kg\n'
                 f'MR = {mutate_rate}, COR = {crossover_rate}, POP = {popu_size}, MAXGEN = {max_generations}')
    ax.grid(True)
    line_mean, = ax.plot([], [], 'b', label='mean fitness')
    line_best, = ax.plot([], [], 'r', label='best fitness')
    ax.legend()
    
    # Initialization
    diversity_history = np.zeros(max_generations)
    population = popu_initialize(popu_size, n, min_a_start_index, orbits, dry_mass_0, prop_mass_0, isp, g_0, sd_mass)
    stall_count = 0
    switch_mutation = True
    threshold_std = 0.1  # Threshold for detecting stagnation based on standard deviation
    no_switch_zone = 10  # Number of generations to track for stagnation
    switch_after = 5
    best_fitness_array = np.full(no_switch_zone // 2, np.inf)  # History of best fitness values
    
    # Main GA loop
    for generation in range(max_generations):
        # Evaluate Fitness
        fitness = fitness_evaluate(population, orbits, dry_mass_0, prop_mass_0, isp, g_0, sd_mass)
        
        # Handle Invalid Solutions with Repair Function
        for i in range(popu_size):
            if np.isinf(fitness[i]):
                population[i, :] = repair(population[i, :], orbits, dry_mass_0, prop_mass_0, isp, g_0, sd_mass)
                fitness[i] = fitness_evaluate(population[i:i+1, :], orbits, dry_mass_0, prop_mass_0, isp, g_0, sd_mass)[0]
        
        mean_fitness[generation] = np.mean(fitness)
        best_fitness[generation] = np.min(fitness)
        
        # Update plot
        line_mean.set_data(np.arange(1, generation + 2), mean_fitness[:generation + 1])
        line_best.set_data(np.arange(1, generation + 2), best_fitness[:generation + 1])
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.01)
        
        # Updating fitness and number of generation stall counting
        if generation >= no_switch_zone:
            best_fitness_array = np.roll(best_fitness_array, -1)
            best_fitness_array[-1] = best_fitness[generation]
            if np.std(best_fitness_array) < threshold_std:
                stall_count += 1
            else:
                stall_count = 0  # Restart the counter on improvement of fitness
        else:
            best_fitness_array[generation % len(best_fitness_array)] = best_fitness[generation]
        
        # Call for switch mutation method if stall count reached
        if stall_count >= switch_after:
            switch_mutation = not switch_mutation  # Toggle between the two mutation methods
            stall_count = 0  # Reset the counter after switching
        
        # Diversity calculation through Hamming distance
        pairwise_distances = np.zeros((popu_size, popu_size))
        for i in range(popu_size):
            for j in range(i + 1, popu_size):
                hamming_dist = np.sum(population[i, :] != population[j, :])
                pairwise_distances[i, j] = hamming_dist
                pairwise_distances[j, i] = hamming_dist
        
        # Pairwise mean diversity
        diversity = np.mean(pairwise_distances)
        diversity_history[generation] = diversity
        
        # Selection
        selected_parents = root_parent_select(population, fitness, popu_size)
        
        # Crossover
        child = crossover(selected_parents, popu_size, crossover_rate, min_a_start_index)
        
        # Switch mutation between swapping and inverse
        if switch_mutation:
            child = mutation(child, mutate_rate, min_a_start_index)
        else:
            child = inverse_mutation(child, mutate_rate, min_a_start_index)
        
        # Create New Population
        population = next_popu(population, child, fitness)
        
        # Display best solution every generation
        best_ind = np.argmin(fitness)
        print(f'Generation {generation + 1}: Best fitness = {fitness[best_ind]:.2f}; Stagnation Counter {stall_count}')
        print(f'Best order: {population[best_ind, :]}')
    
    # Final results
    best_ind = np.argmin(fitness)
    final_order = population[best_ind, :]
    print('\nFinal Optimal order of orbit rendezvous:')
    print(final_order)
    
    result = obj_min_spent_prop_mass(final_order, orbits, dry_mass_0, prop_mass_0, isp, g_0, sd_mass, store=True)
    spent_prop_mass_total, total_mass_change, prop_mass_change, dry_mass_fraction, prop_mass_fraction, stp_mass = result
    
    print(f'\nTotal spent propellant mass for the final optimal order: {spent_prop_mass_total:.2f}')
    print('Change in total mass for each step:')
    print(total_mass_change)
    
    # Plot propellant mass change
    plt.figure()
    plt.plot(range(1, n + 1), prop_mass_change, 'or')
    for i in [0, n - 1]:
        plt.text(i + 1, prop_mass_change[i], f'{prop_mass_change[i]:.2f}',
                 verticalalignment='bottom', horizontalalignment='right')
    plt.xticks(range(1, n + 1), final_order)
    plt.xlabel('Orbit Number')
    plt.ylabel('Mass values in kg')
    plt.legend(['Propellant Mass'])
    plt.title(f'VARIATION OF PROP MASS with SD Mass = {sd_mass} Kg\n'
              f'MR = {mutate_rate}, COR = {crossover_rate}, POP = {popu_size}, MAXGEN = {max_generations}')
    plt.ylim([np.min(prop_mass_change) - 200, np.max(prop_mass_change) + 400])
    plt.grid(True)
    
    # Plot total mass change
    plt.figure()
    plt.plot(range(1, n + 1), total_mass_change, 'ob')
    for i in [0, n - 1]:
        plt.text(i + 1, total_mass_change[i], f' {total_mass_change[i]:.2f}',
                 verticalalignment='bottom', horizontalalignment='left')
    plt.xticks(range(1, n + 1), final_order)
    plt.xlabel('Orbit Number')
    plt.ylabel('Mass values in kg')
    plt.legend(['Total Mass'])
    plt.title(f'VARIATION OF TOTAL MASS with SD Mass = {sd_mass} Kg\n'
              f'MR = {mutate_rate}, COR = {crossover_rate}, POP = {popu_size}, MAXGEN = {max_generations}')
    plt.ylim([np.min(total_mass_change) - 1000, np.max(total_mass_change) + 2000])
    plt.grid(True)
    
    # Diversity history plot
    plt.figure()
    plt.plot(range(1, max_generations + 1), diversity_history, 'g-', linewidth=2)
    plt.xlabel('Generation number')
    plt.ylabel('Diversity')
    plt.title('Diversity of Population Over Generations')
    plt.grid(True)
    
    plt.ioff()
    plt.show()
    
    return final_order, spent_prop_mass_total


if __name__ == "__main__":
    final_order, spent_mass = run_ga()
