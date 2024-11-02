% Fitness evaluation function
function fitness = fitness_evalu_spent_prop_mass(population, orbits, dry_mass_0, Prop_mass_0, Isp, g_0,SD_mass)
    popu_size = size(population, 1);
    fitness = zeros(popu_size, 1);
    
    for i = 1:popu_size
        order = population(i, :);
        spent_prop_mass_total = obj_min_spent_prop_mass(order, orbits, dry_mass_0, Prop_mass_0, Isp, g_0, SD_mass, false);
        fitness(i) = spent_prop_mass_total;
    end
end