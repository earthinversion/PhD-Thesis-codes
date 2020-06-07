function [dobs, dpre]=read_arrivaltimes(filename)
    %% Initialize variables.
%     filename = 'arrival_times.csv';
    delimiter = ',';
    startRow = 2;

    %% Format for each line of text:
    formatSpec = '%f%f%[^\n\r]';

    %% Open the text file.
    fileID = fopen(filename,'r');

    %% Read columns of data according to the format.
    dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'HeaderLines' ,startRow-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');

    %% Close the text file.
    fclose(fileID);

    %% Post processing for unimportable data.

    %% Create output variable
    arrivaltimes = table(dataArray{1:end-1}, 'VariableNames', {'dobs','d_pre'});

    %% Clear temporary variables
    clearvars filename delimiter startRow formatSpec fileID dataArray ans;
    arrivaltimes = table2array(arrivaltimes);
    dobs = arrivaltimes(:,1);
    dpre = arrivaltimes(:,2);