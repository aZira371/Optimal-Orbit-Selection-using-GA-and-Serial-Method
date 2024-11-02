clear;
clc;
close all;
dry_mass_0 = 795; % Initial dry mass in kg
Prop_mass_0 = 2700; % Propellant mass in kg
SD_mass = 0; % Space debris mass in kg, 45.3 for PM and 1486.542 for RB
Isp = 300; % Specific impulse in seconds
g_0 = 9.81; % Gravitational acceleration at Earth's surface in m/s^2
% Inclinations in the first column, Semi-Major Axes in the second column
orbitparam = twoLE_2_orbparam('Targeted_SDs_2LE.txt');
orbits = orbitparam(1:5,[3,1]);
N = length(orbits);
mu = 398600;

% Determine the starting orbit:
% Find the index of the orbit with the minimum semi-major axis
[min_a, min_aIndex] = min(orbits(:, 2));

% Check if all semi-major axes are equal
% If all semi-major axes are equal, choose the orbit with the minimum inclination
% Otherwise, choose the orbit with the minimum semi-major axis
if all(orbits(:, 2) == min_a)
    [~, min_i_index] = min(orbits(:, 1));
    start_index = min_i_index;
else
    start_index = find(orbits(:, 2) == min_a, 1);
end

% Generate all possible permutations of visiting the remaining 4 orbits
to_visit = setdiff(1:N, start_index);
permutations = perms(to_visit);
stp_mass = zeros(24,5);
total_mass_change = zeros(24,5);
prop_mass_change = zeros(24,5);
dry_mass_fraction = zeros(24,5);
prop_mass_fraction = zeros(24,5);
optimal_perm = [];
final_array = zeros(24,6);
for i = 1:size(permutations, 1)
    test_perm = [start_index, permutations(i, :)];
    
    % Calculate the total delta-v for the current permutation
    totalDeltaV = 0;
    spent_prop_mass_total = 0;
    dry_mass = dry_mass_0;
    Prop_mass = Prop_mass_0;
    for j = 2:5
        % Indices of the orbits in the permutation
        orbit1 = test_perm(j-1);
        orbit2 = test_perm(j);
        
        inc1 = orbits(orbit1, 1);
        inc2 = orbits(orbit2, 1);
        a1 = orbits(orbit1, 2);
        a2 = orbits(orbit2, 2);
        % Add SD
        dry_mass = dry_mass + SD_mass;
        % Plane change delta-v 
        deltaV = plane_change(inc1,inc2,a1,a2);
        % total delta-v
        totalDeltaV = totalDeltaV + deltaV;
        % rocket equation
        spent_prop_mass = (dry_mass + Prop_mass)*(1 - exp(-deltaV / (Isp * g_0)));
        spent_prop_mass_total = spent_prop_mass_total + spent_prop_mass;
        Prop_mass = Prop_mass - spent_prop_mass;% update of prop mass after the burn
        stp_mass (i,j) = spent_prop_mass_total;
        total_mass_change(i,j) = dry_mass + Prop_mass;
        prop_mass_change (i,j) = Prop_mass;
        dry_mass_fraction (i,j) = dry_mass/(dry_mass + Prop_mass);
        prop_mass_fraction (i,j) = Prop_mass/(dry_mass + Prop_mass);
        dry_mass_fraction(i,1) = dry_mass_0/(dry_mass_0 + SD_mass + Prop_mass_0);
        prop_mass_fraction(i,1) = Prop_mass_0/(dry_mass_0 + SD_mass + Prop_mass_0);
        total_mass_change(i,1) = dry_mass_0 + SD_mass + Prop_mass_0;
        prop_mass_change(i,1) = Prop_mass_0;
        final_array(i,1) = start_index;
        final_array(i,j) = orbit2;
    end
    final_array(i,6) = stp_mass (i,5);
    if i == 1 || spent_prop_mass_total < min_STP
        min_STP = spent_prop_mass_total;
        optimal_perm = test_perm;
    end
    if spent_prop_mass_total > Prop_mass_0
        disp('Propellant mass spent is more than carried')
        return
    end
end
[~,final_index] = min(final_array(:,6)); 
disp('Minimum Propellant Mass Spent:');
disp(min_STP);

disp('Best Permutation (Orbit Order):');
disp(optimal_perm);

disp('Corresponding Inclinations and Semi-Major Axes:');
disp(orbits(optimal_perm, :));

figure;
plot(1:N, prop_mass_change(final_index,:), 'or');
k=[1,N];
for i = k
    text(i, prop_mass_change(final_index,i), sprintf('%.2f', prop_mass_change(final_index,i)), ...
        'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
end
xticks(1:N);
xticklabels(optimal_perm);
xlabel('Orbit Number');
ylabel('Mass values in kg');
legend('Propellant Mass');
title('VARIATION OF PROP MASS with SD Mass  = 0 Kg','BRUTE FORCE PERMUTATION');
ylim([min(prop_mass_change(final_index,:))-150, max(prop_mass_change(final_index,:))+200]);
grid on;
% saveas(gcf, 'PROP_MASS_CHANGE_50_switching', 'png');


figure;
plot(1:N, total_mass_change(final_index,:), 'ob');
k=[1,N];
for i = k
    text(i, total_mass_change(final_index,i), sprintf(' %.2f', total_mass_change(final_index,i)), ...
        'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'left');
end
xticks(1:N);
xticklabels(optimal_perm);
xlabel('Orbit Number');
ylabel('Mass values in kg');
legend('Total Mass');
title('VARIATION OF TOTAL MASS with SD Mass  = 0 Kg', 'BRUTE FORCE PERMUTATION');
ylim([min(total_mass_change(final_index,:))-100, max(total_mass_change(final_index,:))+400]);
grid on;