"""
TLE (Two-Line Element) Parser Module

Converts 2LE (Two-Line Element) data to orbital parameters.
Note: This parser expects 2LE format (without satellite name lines),
where each satellite is represented by exactly 2 lines.
"""

import numpy as np


def tle_to_orbital_params(filename: str) -> np.ndarray:
    """
    Parse 2LE file and extract orbital parameters.
    
    This function expects the 2LE format where each satellite has exactly 2 lines:
    - Line 1: Satellite catalog number, classification, launch info, epoch, etc.
    - Line 2: Orbital elements (inclination, RAAN, eccentricity, etc.)
    
    Note: This is NOT the standard 3-line TLE format that includes a satellite name.
    
    Args:
        filename: Path to the 2LE file
        
    Returns:
        numpy array with columns: [a, e, inclination, raan, arg_perigee, mean_anomaly]
        where a is semi-major axis in km
    """
    mu = 398600  # km^3/s^2
    
    with open(filename, 'r') as f:
        tle_data = f.read()
    
    tle_lines = tle_data.strip().split('\n')
    num_orbits = len(tle_lines) // 2
    
    a = np.zeros(num_orbits)
    e = np.zeros(num_orbits)
    inclinations = np.zeros(num_orbits)
    raan = np.zeros(num_orbits)
    argument_perigee = np.zeros(num_orbits)
    mean_anomaly = np.zeros(num_orbits)
    
    for i in range(num_orbits):
        line2 = tle_lines[2 * i + 1]  # 2nd line (0-indexed, so line1 is at 2*i, line2 at 2*i+1)
        
        inclinations[i] = float(line2[8:16])
        raan[i] = float(line2[17:25])
        e[i] = float('0.' + line2[26:33])
        argument_perigee[i] = float(line2[34:42])
        mean_anomaly[i] = float(line2[43:51])
        mean_motion_revspd = float(line2[52:63])  # revs per day
        mean_motion_rad_s = mean_motion_revspd * 2 * np.pi / 86400
        a[i] = (mu / (mean_motion_rad_s ** 2)) ** (1/3)
    
    orbital_params = np.column_stack([a, e, inclinations, raan, argument_perigee, mean_anomaly])
    return orbital_params


if __name__ == "__main__":
    # Test the parser
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tle_file = os.path.join(script_dir, '..', 'Targeted_SDs_2LE.txt')
    
    if os.path.exists(tle_file):
        params = tle_to_orbital_params(tle_file)
        print("Orbital Parameters (first 5 orbits):")
        print("Semi-major axis (km), Eccentricity, Inclination (deg), RAAN (deg), Arg Perigee (deg), Mean Anomaly (deg)")
        print(params[:5])
    else:
        print(f"TLE file not found: {tle_file}")
