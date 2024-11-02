function child = scram_mutation(child, mutate_rate, min_a_start_index)
    [popu_size, N] = size(child);
    
    for i = 1:popu_size
        if rand < mutate_rate
            % Select a random subset of genes to scramble
            % Ensure the subset does not include the start index
            subset_length = randi([2, N-1]); 
            subset_start = randi([2, N - subset_length + 1]); 
            
            % Define the subset indices
            subset_indices = subset_start:(subset_start + subset_length - 1);
            
            % shuffle the selected subset of genes
            scrambled_subset = child(i, subset_indices(randperm(length(subset_indices))));
            
            % Replace the original subset in the chromosome with the scrambled one
            child(i, subset_indices) = scrambled_subset;
        end
    end
end
