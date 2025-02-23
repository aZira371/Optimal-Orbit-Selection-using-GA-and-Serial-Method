% population initialization function
function population = popu_initialize_valid(popu_size, N, min_a_start_index,orbits, dry_mass_0, Prop_mass_0, Isp, g_0,SD_mass)
    population = zeros(popu_size, N);
    for i = 1:popu_size
        validity = false;
        while ~validity
            % Generate a list of indices excluding the fixed starting index
             remaining_indices = setdiff(1:N, min_a_start_index);
    
            
                % Start with the fixed starting index
                perm_order = [min_a_start_index, remaining_indices(randperm(length(remaining_indices)))];
             if check_validity(perm_order, orbits, dry_mass_0, Prop_mass_0, Isp, g_0,SD_mass)
                    population(i, :) = perm_order;
                    validity = true;
               
            end
        end   
    end
end