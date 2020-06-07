clear all; close all; clc
files=dir('*.dat'); %files to be read
cmap = colormap(parula(length(files))); 
sumModel_rgh=zeros(160,1);
all_mrgh=[]; 
periods=[];


for i=1:length(files)
    C = strsplit(files(i).name,'.');
    filename=C{1};
    period=strsplit(filename,'_');
    periods=[periods period(end)];
    fileID = fopen(sprintf('%s.dat',filename),'r'); %opening the file in reading mode

    formatSpec = '%f %f'; %defining the format of the data

    sizeA = [2 Inf]; %defining the size of the data

    A = fscanf(fileID,formatSpec,sizeA); %reading the data using fscanf function

    fclose(fileID); %closing the file
    data=A'; %displaying the data
    rgh=data(:,1);
    model_rgh=data(:,2);
    all_mrgh=[all_mrgh model_rgh];
    h(i)=plot(rgh,model_rgh, 'Color',cmap(i,:),'LineWidth',0.5);
%     grid on
    hold on
    
   sumModel_rgh=sumModel_rgh+model_rgh;
end
avgmodelrgh=sumModel_rgh/length(files);
plot(rgh,avgmodelrgh,'b','LineWidth',2)
uperr=avgmodelrgh+2*std(all_mrgh')';
dwnerr=avgmodelrgh-2*std(all_mrgh')';
hold on
plot(rgh,uperr,'b--','LineWidth',2)
plot(rgh,dwnerr,'b--','LineWidth',2)
xlabel('Isotropic Smoothing')
ylabel('Model Roughness')
legend([h(1) h(2) h(3) h(4) h(5) h(6) h(7) h(8) h(9) h(10) h(11) h(12) h(13) h(14)],sprintf('%s s',periods{1}),sprintf('%s s ',periods{2}),sprintf('%s s ',periods{3}),sprintf('%s s ',periods{4}),sprintf('%s s ',periods{5})...
    ,sprintf('%s s ',periods{6}),sprintf('%s s ',periods{7}),sprintf('%s s ',periods{8}),sprintf('%s s ',periods{9}),sprintf('%s s ',periods{10})...
    ,sprintf('%s s ',periods{11}),sprintf('%s s ',periods{12}),sprintf('%s s ',periods{13}),sprintf('%s s ',periods{14}))
saveas(gcf,'IsoSmooth.pdf')

