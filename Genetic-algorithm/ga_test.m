clear; close all; clc;

numrun = 2;
output=zeros(numrun,5);
for jj=1:numrun
    close all; clc;
    lower=[-3 -3 -3 5 -1];
    upper=[3 3 0 7 1]; 


    % options = optimoptions('ga','PlotFcn', @gaplotbestf,'Display','iter');
%     options = optimoptions('ga','PlotFcn', @gaplotbestf);
%     x=ga(@(pp)fit_arrival_times(pp),5,[],[],[],[],lower,upper,[],options)
    x=ga(@(pp)fit_arrival_times(pp),5,[],[],[],[],lower,upper,[])

    output(jj,1) = x(1);
    output(jj,2) = x(2);
    output(jj,3) = x(3);
    output(jj,4) = x(4);
    output(jj,5) = x(5);
end
output
