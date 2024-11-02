function child = inverse_mutation(child, mutate_rate, min_a_start_index)
    [popu_size, N] = size(child);
    
    for i = 1:popu_size
        if rand < mutate_rate
            % Select a random subset of genes to invert
            % Ensure the first index is maintaned
            subset_length = randi([2, N-1]); % Random length of the subset with minimum 2 genes
            subset_start = randi([2, N - subset_length + 1]); % Start of the subset
            
            % Define the subset indices
            subset_indices = subset_start:(subset_start + subset_length - 1);
            
            % Invert the selected subset using flipr
            inverted_subset = child(i, fliplr(subset_indices));
            
            % Replace the original subset in the child with the inverted one
            child(i, subset_indices) = inverted_subset;
        end
    end
end
