clear;
clc;
close all;
dry_mass = 795;
propmass = 2700; 
sysmass = dry_mass + propmass; 
SD_mass = 1500;
I_sp = 300; 
g_sl = 9.81;

orbparam = twoLE_2_orbparam('Targeted_SDs_2LE.txt');
orbits = orbparam(1:21, [3, 1]);
N = size(orbits, 1); 
a = orbits(:,2); 
inclinations = orbits(:,1);
SD_number = 1:N;
[~, sorted_indices] = sort(a);
a_sorted = a(sorted_indices);
inclinations_sorted = inclinations(sorted_indices);
SD_number_sorted = SD_number(sorted_indices);
current_orbit = 1; 
visited = false(1, N);
visited(current_orbit) = true;
sequence = SD_number_sorted(current_orbit); 
total_delta_v = 0; 
% Initialize for first orbit
prop_mass_change = zeros(1, N);
total_mass_change = zeros(1, N);
prop_mass_change(1) = propmass;
total_mass_change(1) = dry_mass + propmass;

for i = 1:N-1
    spent_prop_mass_o = inf;
    delta_v_opti = inf;
    selected_orbit = -1;

    for j = 1:N
        if ~visited(j)
            % Calculate delta-v for the plane change
            delta_v = plane_change_GA(inclinations_sorted(current_orbit), inclinations_sorted(j), a_sorted(current_orbit), a_sorted(j));
            
            % Calculate the propellant mass spent for this maneuver
            dry_mass_with_SD = dry_mass + SD_mass; % Add SD mass
            spent_prop_mass = (dry_mass_with_SD + propmass)*(1 - exp(-delta_v / (I_sp * g_sl)));
            
            % Skip invalid fuel mass
            if spent_prop_mass <= propmass && spent_prop_mass < spent_prop_mass_o
                spent_prop_mass_o = spent_prop_mass;
                delta_v_opti = delta_v;
                selected_orbit = j;
            end
        end
    end
    
    % update data for valid answer
    if selected_orbit ~= -1
        sequence = [sequence, SD_number_sorted(selected_orbit)];
        total_delta_v = total_delta_v + delta_v_opti;

        % mass update
        propmass = propmass - spent_prop_mass_o;
        dry_mass = dry_mass + SD_mass; 
        prop_mass_change(i+1) = propmass;
        total_mass_change(i+1) = dry_mass + propmass;
        
        % visit update
        current_orbit = selected_orbit;
        visited(current_orbit) = true;
    else
%no solution break
        break;
    end
end

disp('Optimal sequence of orbit rendezvous based on original IDs:');
disp(sequence);
disp(['Total delta-V required: ', num2str(total_delta_v), ' m/s']);
disp('Propellant mass after each rendezvous:');
disp(prop_mass_change(1:length(sequence)));
disp('Total mass after each rendezvous:');
disp(total_mass_change(1:length(sequence)));

figure;
plot(1:length(sequence), total_mass_change(1:length(sequence)), 'ob');
k=[1,length(sequence)];
for i = k
    text(i, total_mass_change(i), sprintf(' %.2f', total_mass_change(i)), ...
        'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'left');
end
xticks(1:N);
xticklabels(sequence);
xlabel('Orbit Number');
ylabel('Mass values in kg');
title('VARIATION OF TOTAL MASS orbit by orbit with SD Mass = 1500 kg', 'SERIES METHOD');
grid on;

figure;
plot(1:length(sequence), prop_mass_change(1:length(sequence)), 'or');
k=[1,length(sequence)];
for i = k
    text(i, prop_mass_change(i), sprintf('%.2f', prop_mass_change(i)), ...
        'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
end
xticks(1:N);
xticklabels(sequence);
xlabel('Orbit Number');
ylabel('Mass values in kg');
title('VARIATION OF PROP MASS orbit by orbit with SD Mass = 1500 kg', 'SERIES METHOD');
grid on;