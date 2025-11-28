"""
Orbital Mechanics Module

Contains functions for orbital maneuver calculations.
"""

import numpy as np


def plane_change(inc_1: float, inc_2: float, a_1: float, a_2: float) -> float:
    """
    Calculate delta-V for a combined plane change and altitude change maneuver.
    
    Args:
        inc_1: Initial inclination in degrees
        inc_2: Final inclination in degrees
        a_1: Initial semi-major axis in km
        a_2: Final semi-major axis in km
        
    Returns:
        Delta-V in m/s
    """
    theta_1 = np.radians(inc_1)
    theta_2 = np.radians(inc_2)
    
    mu = 398600  # km^3/s^2
    v1 = np.sqrt(mu / a_1)  # km/s
    v2 = np.sqrt(mu / a_2)  # km/s
    
    # Inclination change
    del_theta = abs(theta_2 - theta_1)
    delta_v = np.sqrt(v1**2 + v2**2 - 2 * v1 * v2 * np.cos(del_theta))
    delta_v = delta_v * 1000  # Convert to m/s
    
    return delta_v


if __name__ == "__main__":
    # Test the plane change function
    dv = plane_change(82.5, 82.0, 6800, 6900)
    print(f"Delta-V for test maneuver: {dv:.2f} m/s")
