% population initialization function
function population = popu_initialize(popu_size, N, min_a_start_index,orbits, dry_mass_0, Prop_mass_0, Isp, g_0,SD_mass)
    population = zeros(popu_size, N);
    for i = 1:popu_size
            remaining_indices = setdiff(1:N, min_a_start_index);
            perm_order = [min_a_start_index, remaining_indices(randperm(length(remaining_indices)))];
            population(i,:) = perm_order;% Ensure fixed start orbit is first
    end
end