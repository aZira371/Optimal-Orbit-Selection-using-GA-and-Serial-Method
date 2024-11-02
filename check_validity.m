%validity check function
function [validity] = check_validity(order, orbits, dry_mass_0, Prop_mass_0, Isp, g_0, SD_mass)
    validity = true;
    dry_mass = dry_mass_0;
    Prop_mass = Prop_mass_0;
    spent_prop_mass_total = 0;
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
            % rocket equation
        spent_prop_mass = (dry_mass + Prop_mass)*(1 - exp(-delta_v / (Isp * g_0)));
        spent_prop_mass_total = spent_prop_mass_total + spent_prop_mass;
        Prop_mass = Prop_mass - spent_prop_mass;% update of prop mass after the burn
        if Prop_mass < 0 
            validity = false;
            return;
        end
    end
end