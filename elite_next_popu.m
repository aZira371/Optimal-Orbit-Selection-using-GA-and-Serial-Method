% Next population creation
function new_popu = elite_next_popu(prev_popu, child, fitness)
    [popu_size, ~] = size(prev_popu);
    
    % preserve 10% of population
    preserve_count = ceil(0.1 * popu_size);
    
    % 90% population will be children
    child_count = popu_size - preserve_count;
    
    % sort based on fitness
    [~, best_order_indices] = sort(fitness, 'ascend');
    
    % allot preserve fraction to new population
    preserved_popu = prev_popu(best_order_indices(1:preserve_count), :);
    
    % rest all is children
    new_popu = [preserved_popu; child(1:child_count, :)];
end
