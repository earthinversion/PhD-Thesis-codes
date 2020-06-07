clear all; close all; clc
files=dir('*.dat'); %files to be read
sumModel_rgh=zeros(160,1);
for i=1:length(files)
    C = strsplit(files(i).name,'.');
    filename=C{1};
    fileID = fopen(sprintf('%s.dat',filename),'r'); %opening the file in reading mode

    formatSpec = '%f %f'; %defining the format of the data

    sizeA = [2 Inf]; %defining the size of the data

    A = fscanf(fileID,formatSpec,sizeA); %reading the data using fscanf function

    fclose(fileID); %closing the file

    data=A'; %displaying the data
    rgh=data(:,1);
    model_rgh=data(:,2);
%     figure(1)
%     plot(rgh,model_rgh,'*--')
%     xlabel('Smoothing')
%     ylabel('Model Roughness')
%     grid on
%     hold on
   
    
    sumModel_rgh=sumModel_rgh+model_rgh;
    
end
avgmodelrgh=sumModel_rgh/length(files);

h1=plot(rgh,avgmodelrgh,'--','LineWidth',2)
     %%Calculating curvature 
  dx = gradient(rgh);
ddx = gradient(dx);
dy = gradient(avgmodelrgh);
ddy = gradient(dy);

num = dx .* ddy - ddx .* dy;
denom = dx .* dx + dy .* dy;
denom = sqrt(denom);
denom = denom .* denom .* denom;
curvature = num ./ denom;
curvature(denom < 0) = NaN; 
    
    hold on
h2=plot(rgh,30*curvature,'r--','LineWidth',2)
%     grid on
xlabel('Isotropic Smoothing')
ylabel('Model Roughness')
    title(sprintf('Maximum Curvature at = %.2f',rgh(find(curvature==max(curvature)))))
    legend([h1,h2],'L-curve','Curvature')
saveas(gcf,'IsoSmoothCurv.pdf')
