% Mutation function
function child = mutation(child, mutate_rate, min_a_start_index)
    [popu_size, N] = size(child);
    for i = 1:popu_size
        if rand < mutate_rate
            index_swap = randperm(N, 2);
            % Ensure fixed start index is not swapped
            if index_swap(1) ~= 1 && index_swap(2) ~= 1
                % Swap random the elements
                temp_child = child(i, index_swap(1));
                child(i, index_swap(1)) = child(i, index_swap(2));
                child(i, index_swap(2)) = temp_child;
            end
        end
    end
end