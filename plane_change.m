function delta_v = plane_change(inc_1, inc_2, a_1, a_2)
    thet_a_1 = deg2rad(inc_1);
    thet_a_2 = deg2rad(inc_2);
    
    mu = 398600; % km^3/s^2
    v1 = sqrt(mu / a_1); % km/s
    v2 = sqrt(mu / a_2); % km/s
    
    % inclination change
    del_theta = abs(thet_a_2 - thet_a_1);
    delta_v = sqrt(v1^2 + v2^2 - 2 * v1 * v2 * cos(deg2rad(del_theta)));
    delta_v = delta_v * 1000; % m/s
end