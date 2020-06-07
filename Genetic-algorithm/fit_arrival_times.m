function E=fit_arrival_times(pp)
    filename = 'arrival_times.csv';
    [dobs, dpre] = read_arrivaltimes(filename);
    stationlocations = read_stnloc('station_locations.csv', 2, 31);
%     eq_loc = [2 2 -2];
    d_pre = zeros(length(stationlocations),1);
    for i=1:length(stationlocations)
        dist = sqrt((pp(1) - stationlocations(i,1))^2 + (pp(2) - stationlocations(i,2))^2 + (pp(3) - stationlocations(i,3))^2);
        arr = dist/pp(4) + pp(5);
        d_pre(i) = arr;
    end
    E=sum((dobs-d_pre).^2);