"""
Validity Check Module

Checks if a given orbit visitation order is valid (enough propellant).
"""

import numpy as np
from orbital_mechanics import plane_change


def check_validity(order: np.ndarray, orbits: np.ndarray, dry_mass_0: float,
                   prop_mass_0: float, isp: float, g_0: float, sd_mass: float) -> bool:
    """
    Check if a given order of orbit visits is valid (propellant doesn't run out).
    
    Args:
        order: Array of orbit indices in visitation order (1-indexed for MATLAB compatibility)
        orbits: Array of orbit parameters [inclination, semi-major axis]
        dry_mass_0: Initial dry mass in kg
        prop_mass_0: Initial propellant mass in kg
        isp: Specific impulse in seconds
        g_0: Gravitational acceleration at Earth's surface in m/s^2
        sd_mass: Space debris mass in kg
        
    Returns:
        True if the order is valid, False otherwise
    """
    dry_mass = dry_mass_0
    prop_mass = prop_mass_0
    
    for i in range(len(order) - 1):
        # Convert to 0-indexed
        ind1 = int(order[i]) - 1
        ind2 = int(order[i + 1]) - 1
        
        inc_1 = orbits[ind1, 0]
        inc_2 = orbits[ind2, 0]
        a_1 = orbits[ind1, 1]
        a_2 = orbits[ind2, 1]
        
        # Add SD mass after picking up debris
        dry_mass = dry_mass + sd_mass
        
        # Compute delta-V
        delta_v = plane_change(inc_1, inc_2, a_1, a_2)
        
        # Rocket equation
        spent_prop_mass = (dry_mass + prop_mass) * (1 - np.exp(-delta_v / (isp * g_0)))
        prop_mass = prop_mass - spent_prop_mass
        
        if prop_mass < 0:
            return False
    
    return True


if __name__ == "__main__":
    # Test validity check
    orbits = np.array([
        [82.5, 6800],
        [82.0, 6900],
        [83.0, 7000],
        [81.5, 6750],
        [82.2, 6850]
    ])
    
    order = np.array([1, 2, 3, 4, 5])
    result = check_validity(order, orbits, 795, 2700, 300, 9.81, 1500)
    print(f"Order validity: {result}")
