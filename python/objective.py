"""
Objective Function Module

Calculates the spent propellant mass for a given orbit visitation order.
"""

import numpy as np
from orbital_mechanics import plane_change


def obj_min_spent_prop_mass(order: np.ndarray, orbits: np.ndarray, dry_mass_0: float,
                            prop_mass_0: float, isp: float, g_0: float, sd_mass: float,
                            store: bool = False):
    """
    Calculate total spent propellant mass for a given order of orbit visits.
    
    Args:
        order: Array of orbit indices in visitation order (1-indexed)
        orbits: Array of orbit parameters [inclination, semi-major axis]
        dry_mass_0: Initial dry mass in kg
        prop_mass_0: Initial propellant mass in kg
        isp: Specific impulse in seconds
        g_0: Gravitational acceleration at Earth's surface in m/s^2
        sd_mass: Space debris mass in kg
        store: If True, return additional mass tracking data
        
    Returns:
        If store=False: spent_prop_mass_total
        If store=True: tuple of (spent_prop_mass_total, total_mass_change, prop_mass_change,
                                 dry_mass_fraction, prop_mass_fraction, stp_mass)
    """
    delta_v_total = 0
    spent_prop_mass_total = 0
    dry_mass = dry_mass_0
    prop_mass = prop_mass_0
    n = len(order)
    
    if store:
        total_mass_change = np.zeros(n - 1)
        prop_mass_change = np.zeros(n - 1)
        dry_mass_fraction = np.zeros(n - 1)
        prop_mass_fraction = np.zeros(n - 1)
        stp_mass = np.zeros(n - 1)
    
    for i in range(n - 1):
        # Convert to 0-indexed
        ind1 = int(order[i]) - 1
        ind2 = int(order[i + 1]) - 1
        
        inc_1 = orbits[ind1, 0]
        inc_2 = orbits[ind2, 0]
        a_1 = orbits[ind1, 1]
        a_2 = orbits[ind2, 1]
        
        # Add SD mass
        dry_mass = dry_mass + sd_mass
        
        # Compute delta-V
        delta_v = plane_change(inc_1, inc_2, a_1, a_2)
        delta_v_total = delta_v_total + delta_v
        
        # Rocket equation
        spent_prop_mass = (dry_mass + prop_mass) * (1 - np.exp(-delta_v / (isp * g_0)))
        spent_prop_mass_total = spent_prop_mass_total + spent_prop_mass
        prop_mass = prop_mass - spent_prop_mass  # Update propellant mass after burn
        
        # Store mass changes if requested
        if store:
            total_mass_change[i] = dry_mass + prop_mass
            prop_mass_change[i] = prop_mass
            dry_mass_fraction[i] = dry_mass / (dry_mass + prop_mass)
            prop_mass_fraction[i] = prop_mass / (dry_mass + prop_mass)
            stp_mass[i] = spent_prop_mass_total
        
        if prop_mass < 0:
            if store:
                return (np.inf, total_mass_change, prop_mass_change,
                        dry_mass_fraction, prop_mass_fraction, stp_mass)
            return np.inf
    
    if store:
        # Prepend initial values
        dry_mass_fraction = np.concatenate([[dry_mass_0 / (dry_mass_0 + sd_mass + prop_mass_0)], dry_mass_fraction])
        prop_mass_fraction = np.concatenate([[prop_mass_0 / (dry_mass_0 + sd_mass + prop_mass_0)], prop_mass_fraction])
        total_mass_change = np.concatenate([[dry_mass_0 + sd_mass + prop_mass_0], total_mass_change])
        prop_mass_change = np.concatenate([[prop_mass_0], prop_mass_change])
        stp_mass = np.concatenate([[0], stp_mass])
        
        return (spent_prop_mass_total, total_mass_change, prop_mass_change,
                dry_mass_fraction, prop_mass_fraction, stp_mass)
    
    return spent_prop_mass_total


if __name__ == "__main__":
    # Test objective function
    orbits = np.array([
        [82.5, 6800],
        [82.0, 6900],
        [83.0, 7000],
        [81.5, 6750],
        [82.2, 6850]
    ])
    
    order = np.array([1, 2, 3, 4, 5])
    result = obj_min_spent_prop_mass(order, orbits, 795, 2700, 300, 9.81, 0, store=True)
    print(f"Spent propellant mass: {result[0]:.2f} kg")
    print(f"Total mass change: {result[1]}")
    print(f"Propellant mass change: {result[2]}")
