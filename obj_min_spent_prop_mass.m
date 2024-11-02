% Objective function 
function [spent_prop_mass_total, total_mass_change, prop_mass_change, dry_mass_fraction, prop_mass_fraction,stp_mass] = obj_min_spent_prop_mass(order, orbits, dry_mass_0, Prop_mass_0, Isp, g_0, SD_mass, store)
    delta_v_total = 0;
    spent_prop_mass_total = 0;
    dry_mass = dry_mass_0;
    Prop_mass = Prop_mass_0;
    total_mass_change = zeros(1, length(order)-1);
    prop_mass_change = zeros(1, length(order)-1);
    dry_mass_fraction = zeros(1, length(order)-1);
    prop_mass_fraction = zeros(1, length(order)-1);
    stp_mass = zeros(1, length(order)-1);
    for i = 1:length(order) - 1
        ind1 = order(i);
        ind2 = order(i + 1);
        inc_1 = orbits(ind1, 1);
        inc_2 = orbits(ind2, 1);
        a_1 = orbits(ind1, 2);
        a_2 = orbits(ind2, 2);
        % Add SD
        dry_mass = dry_mass + SD_mass;
        % Compute delta-V 
        delta_v = plane_change(inc_1, inc_2, a_1, a_2);
        delta_v_total = delta_v_total + delta_v;
        % rocket equation
        spent_prop_mass = (dry_mass + Prop_mass)*(1 - exp(-delta_v / (Isp * g_0)));
        spent_prop_mass_total = spent_prop_mass_total + spent_prop_mass;
        Prop_mass = Prop_mass - spent_prop_mass;% update of prop mass after the burn
        % Store the mass change 
        if store
            total_mass_change(i) = dry_mass + Prop_mass;
        end
        if store
            prop_mass_change (i) = Prop_mass;
            dry_mass_fraction (i) = dry_mass/(dry_mass + Prop_mass);
            prop_mass_fraction (i) = Prop_mass/(dry_mass + Prop_mass);
            stp_mass (i) = spent_prop_mass_total;
        end

        if Prop_mass < 0
            spent_prop_mass_total = inf; 
            return; 
        end
    end
    
    if store
        dry_mass_fraction = [dry_mass_0/(dry_mass_0 + SD_mass + Prop_mass_0), dry_mass_fraction];
        prop_mass_fraction = [Prop_mass_0/(dry_mass_0 + SD_mass + Prop_mass_0), prop_mass_fraction];
        total_mass_change = [dry_mass_0 + SD_mass + Prop_mass_0,total_mass_change];
        prop_mass_change = [Prop_mass_0, prop_mass_change];
        stp_mass = [0,stp_mass];
    end
end