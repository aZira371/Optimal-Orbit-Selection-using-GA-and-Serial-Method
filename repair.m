function repaired_order = repair(order, orbits, dry_mass_0, Prop_mass_0, Isp, g_0, SD_mass)
    repaired_order = order;
    max_attempts = 100; % Maximum number of attempts before restarting
    attempt_count = 0;

    while true
        if check_validity(repaired_order, orbits, dry_mass_0, Prop_mass_0, Isp, g_0, SD_mass)
            break;
        end
        
        % Increase attempt count
        attempt_count = attempt_count + 1;

        % If too many attempts, restart with a new random order
        if attempt_count > max_attempts
            repaired_order = [repaired_order(1), randperm(length(order) - 1) + 1];
            attempt_count = 0;
            continue;
        end

        % Choose a modification type: reverse or shuffle a subsequence
        modification_type = randi(2);

        % Define the indices for the subsequence, excluding the first index
        start_idx = randi(length(order) - 1) + 1; % Random start index between 2 and N
        max_length = length(order) - start_idx; % Maximum length of subsequence
        
        % Ensure valid subsequence length
        if max_length >= 1
            length_subseq = randi([2, max_length + 1]); % Length of subsequence between 2 and max_length
            end_idx = start_idx + length_subseq - 1; % End index of subsequence

            % Ensure end_idx does not exceed the length of the order
            if end_idx > length(order)
                end_idx = length(order);
            end

            switch modification_type
                case 1 % Reverse a random subsequence
                    repaired_order(start_idx:end_idx) = ...
                        fliplr(repaired_order(start_idx:end_idx));

                case 2 % Shuffle a random subsequence
                    subsequence = repaired_order(start_idx:end_idx);
                    repaired_order(start_idx:end_idx) = ...
                        subsequence(randperm(length(subsequence)));
            end
        end
    end
end
