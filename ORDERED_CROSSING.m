function child = ORDERED_CROSSING(parent1, parent2, crossover_location, N, min_a_start_index)
    % Initialize the child with zeros
    child = zeros(1, N);
    % Set the first index to the fixed start orbit
    child(1) = min_a_start_index;
    
    % Create segments from the selected parents
    segment = parent1(2:crossover_location);
    remaining = setdiff(parent2(2:end), segment, 'stable');
    
    % Create the child sequence
    child(2:crossover_location) = segment;
    
    % Ensure remaining fits exactly into the rest of the child array
    % Calculate the number of remaining slots in the child
    remaining_slots = N - crossover_location;
    
    % Fill the remaining slots in the child with the 'remaining' sequence
    child(crossover_location+1:end) = remaining(1:remaining_slots);
end
