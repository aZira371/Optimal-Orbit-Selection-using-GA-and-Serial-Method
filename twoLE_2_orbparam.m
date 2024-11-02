function [orbital_params] = twoLE_2_orbparam(filename)
    mu = 398600;
    tle_data = fileread(filename);
    tle_lines = strsplit(tle_data, '\n');
    num_orbits = length(tle_lines) / 2;
    a = zeros(num_orbits, 1);
    e = zeros(num_orbits, 1);
    inclinations = zeros(num_orbits, 1);
    raan = zeros(num_orbits, 1);
    argument_perigee = zeros(num_orbits, 1);
    mean_anomaly = zeros(num_orbits, 1);
    mean_motion = zeros(num_orbits, 1);

    for i = 1:num_orbits
        line2 = tle_lines{2*i};   % 2nd line

        inclinations(i) = str2double(line2(9:16));
        raan(i) = str2double(line2(18:25));
        e(i) = str2double(['0.', line2(27:33)]);
        argument_perigee(i) = str2double(line2(35:42));
        mean_anomaly(i) = str2double(line2(44:51));
        mean_motion_revspd = str2double(line2(53:63)); % revs per day
        mean_motion(i) = mean_motion_revspd;
        mean_motion_rad_s = mean_motion_revspd * 2 * pi / 86400;
        a(i) = (mu / (mean_motion_rad_s^2))^(1/3);
    end


    orbital_params = [ a, e, inclinations, raan, argument_perigee, mean_anomaly];
end