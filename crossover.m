% Crossover Function
function child = crossover(parents, popu_size, crossover_rate, min_a_start_index)
    [num_parents, N] = size(parents);
    child = zeros(popu_size, N);

    for i = 1:2:popu_size
        if rand < crossover_rate
            parent1 = parents(randi(num_parents), :);
            parent2 = parents(randi(num_parents), :);
            crossover_location = randi([2 N]); % Start from index 2 to ensure min index a start

            % Ordered crossover
            child(i, :) = ORDERED_CROSSING(parent1, parent2, crossover_location, N, min_a_start_index);
            if i+1 <= popu_size
                child(i+1, :) = ORDERED_CROSSING(parent2, parent1, crossover_location, N, min_a_start_index);
            end
        else
            child(i, :) = parents(randi(num_parents), :);
            if i+1 <= popu_size
                child(i+1, :) = parents(randi(num_parents), :);
            end
        end
    end
end