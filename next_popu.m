% Next population creation
function new_popu = next_popu(prev_popu, child, fitness)
    [popu_size, ~] = size(prev_popu);
    [~, best_order_indices] = sort(fitness);
    new_popu = [prev_popu(best_order_indices(1:popu_size/2), :); child(1:popu_size/2, :)];
end