function selected_parents = root_parent_select(population, fitness, popu_size)
    % Rank the population based on fitness (ascending order)
    [~, sorted_indices] = sort(fitness);
    
    % Assign ranks inversely (lower fitness gets higher rank)
    ranks = 1:popu_size;  % Lowest fitness has rank 1, highest fitness has rank popu_size
    
    % Calculate selection values proportional to 1/sqrt(rank)
    raw_selection_values = 1 ./ sqrt(ranks);
    
    % Scale the raw selection values so that their sum equals the population size
    scaled_selection_values = raw_selection_values * (popu_size / sum(raw_selection_values));
    
    % Determine the number of parents each individual should produce
    expected_counts = scaled_selection_values;
    
    % Initialize the selected parents matrix
    selected_parents = zeros(popu_size, size(population, 2));
    parent_index = 1;
    pointer = rand * (1/popu_size); % Random start
    cumulative_sum = 0;
    
    for i = 1:popu_size
        cumulative_sum = cumulative_sum + expected_counts(i);
        while pointer < cumulative_sum && parent_index <= popu_size
            % Select the corresponding individual from the population
            selected_parents(parent_index, :) = population(sorted_indices(i), :);
            parent_index = parent_index + 1;
            pointer = pointer + 1;
        end
    end
end
