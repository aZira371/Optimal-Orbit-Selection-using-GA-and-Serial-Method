clear;
clc;
close all;
dry_mass_0 = 795; % Initial dry mass in kg
Prop_mass_0 = 2700; % Propellant mass in kg
SD_mass = 1500; % Space debris mass in kg,0 or no SD 50 for PM and 1500 for RB
Isp = 300; % Specific impulse in seconds
g_0 = 9.81; % Gravitational acceleration at Earth's surface in m/s^2
orbparam = twoLE_2_orbparam('Targeted_SDs_2LE.txt');
orbits = orbparam(1:20, [3, 1]);
N = size(orbits, 1); 
lb = ones(1,N);
ub = N*ones(1,N);

% min semi major axis is visited first
[~, min_a_ind] = min(orbits(:, 2));
min_a_start_index = min_a_ind;

% GA settings
popu_size = 500; % Population size
max_generations = 250; % Number of generations
mutate_rate = 0.9; % Mutation rate
crossover_rate = 0.9; % Crossover rate
mean_fitness = zeros(max_generations, 1);
best_fitness = zeros(max_generations, 1);

% live plot of fitness values 
figure;
hold on;
plot_of_mean = plot(NaN, NaN, 'b');
plot_of_best = plot(NaN, NaN, 'r');
xlabel('Generation number')
ylabel('Fitness values')
legend('mean fitness', 'best fitness');
title('VARIATION OF FITNESS GENERATION BY GENERATION with SD Mass  = 1500 Kg', 'MR = 0.9, COR = 0.9, POP = 50, MAXGEN = 250');
grid on;
%saveas(gcf,'fitness 45.3 switching','png')

% initialization
diversity_history = zeros(max_generations, 1);
population = popu_initialize(popu_size, N, min_a_start_index, orbits, dry_mass_0, Prop_mass_0, Isp, g_0,SD_mass);
stall_count = 0;
switch_mutation = true;  
threshold_std = 0.1;   % Threshold for detecting stagnation based on standard deviation
no_switch_zone = 10;  % Number of generations to track for stagnation
switch_after = 5;
best_fitness_array = inf(no_switch_zone/2, 1); % History of best fitness values

% Main GA loop
for generation = 1:max_generations

    % Evaluate Fitness
    fitness = fitness_evalu_spent_prop_mass(population, orbits, dry_mass_0, Prop_mass_0, Isp, g_0,SD_mass);
    
            % Handle Invalid Solutions with Repair Function
    for i = 1:popu_size
        if isinf(fitness(i))
            population(i, :) = repair(population(i, :), orbits, dry_mass_0, Prop_mass_0, Isp, g_0,SD_mass);
            fitness(i) = fitness_evalu_spent_prop_mass(population(i, :), orbits, dry_mass_0, Prop_mass_0, Isp, g_0,SD_mass);
        end
    end

    mean_fitness(generation) = mean(fitness);
    best_fitness(generation) = min(fitness);
    set(plot_of_mean, 'XData', 1:generation, 'YData', mean_fitness(1:generation));
    set(plot_of_best, 'XData', 1:generation, 'YData', best_fitness(1:generation));
    drawnow;
    
    % Updating fitness and number of generation stall counting
    if generation > no_switch_zone
        best_fitness_array = [best_fitness_array(2:end); best_fitness(generation)];
        if std(best_fitness_array) < threshold_std
            stall_count = stall_count + 1;
        else
            stall_count = 0; % Rstarting the counter on improvement of fitness
        end
    else
        best_fitness_array(mod(generation - 1, no_switch_zone) + 1) = best_fitness(generation);
    end
    
    % call for switch mutation method if stall count reached
    if stall_count >= switch_after
        switch_mutation = ~switch_mutation; % Toggle between the two mutation methods
        stall_count = 0; % Reset the counter after switching
    end
    
    % Diversity calculation through hamming distance
    pairwise_distances = zeros(popu_size, popu_size); % Matrix to store pairwise distances
    for i = 1:popu_size
        for j = i+1:popu_size
            % Calculate Hamming distance between population(i, :) and population(j, :)
            hamming_dist = sum(population(i, :) ~= population(j, :));
            pairwise_distances(i, j) = hamming_dist;
            pairwise_distances(j, i) = hamming_dist; 
        end
    end
    
    % pairwise mean diversity
    diversity = mean(pairwise_distances(:));
    diversity_history(generation) = diversity; % diversity storage
    % Selection
    selected_parents = root_parent_select(population, fitness, popu_size);
    % Crossover
    child = crossover(selected_parents, popu_size, crossover_rate, min_a_start_index);
    % switch mutation between swapping and inverse
    if switch_mutation
        child = mutation(child, mutate_rate, min_a_start_index);
    else
        child = inverse_mutation(child, mutate_rate, min_a_start_index);
    end

    
    % Create New Population
    population = next_popu(population, child, fitness);
    
    % Display best solution every generation
    [~, best_ind] = min(fitness);
    disp(['Generation ', num2str(generation), ': Best fitness = ', num2str(fitness(best_ind)), '; Stagnation Counter ', num2str(stall_count)]);
    disp(['Best order: ', num2str(population(best_ind, :))]);
end


% final results
[~, best_ind] = min(fitness);
final_order = population(best_ind, :);
disp('Final Optimal order of orbit rendezvous:');
disp(final_order);
[spent_prop_mass_total, total_mass_change, prop_mass_change, dry_mass_fraction, prop_mass_fraction, stp_mass] = obj_min_spent_prop_mass(final_order, orbits, dry_mass_0, Prop_mass_0, Isp, g_0, SD_mass, true);
disp(['Total spent propellant mass for the final optimal order: ', num2str(spent_prop_mass_total) ]);
disp('Change in total mass for each step:');
disp(total_mass_change);

figure;
plot(1:N, prop_mass_change, 'or');
k=[1,N];
for i = k
    text(i, prop_mass_change(i), sprintf('%.2f', prop_mass_change(i)), ...
        'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
end
xticks(1:N);
xticklabels(final_order);
xlabel('Orbit Number');
ylabel('Mass values in kg');
legend('Propellant Mass');
title('VARIATION OF PROP MASS with SD Mass  = 1500 Kg', 'MR = 0.9, COR = 0.9, POP = 50, MAXGEN = 250');
ylim([min(prop_mass_change)-200, max(prop_mass_change)+400]);
grid on;
% saveas(gcf, 'PROP_MASS_CHANGE_50_switching', 'png');


figure;
plot(1:N, total_mass_change, 'ob');
k=[1,N];
for i = k
    text(i, total_mass_change(i), sprintf(' %.2f', total_mass_change(i)), ...
        'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'left');
end
xticks(1:N);
xticklabels(final_order);
xlabel('Orbit Number');
ylabel('Mass values in kg');
legend('Total Mass');
title('VARIATION OF TOTAL MASS with SD Mass  = 1500 Kg', 'MR = 0.9, COR = 0.9, POP = 50, MAXGEN = 250');
ylim([min(total_mass_change)-1000, max(total_mass_change)+2000]);
grid on;
% saveas(gcf, 'TOTAL_MASS_CHANGE_50_switching', 'png');

% figure;
% plot(1:N, dry_mass_fraction,'ob');
% hold on;
% plot(1:N, prop_mass_fraction, 'or');
% xticks(1:N);
% xticklabels(final_order);
% xlabel('Orbit Number')
% ylabel('Mass fraction')
% legend('Dry Mass Fraction', 'Propellant Mass Fraction');
% title('VARIATION OF MASS FRACTIONS ORBIT BY ORBIT for 21 orbits with SD Mass  = 45.3 Kg', 'MR = 0.9, COR = 0.9, POP = 10, MAXGEN = 50');
% grid on;
%saveas(gcf,'mass fractions PM switching','png')

% diversity history plot
figure;
plot(1:max_generations, diversity_history, 'g-', 'LineWidth', 2);
xlabel('Generation number');
ylabel('Diversity');
title('Diversity of Population Over Generations');
grid on;
%saveas(gcf,'diversity PM switching','png')