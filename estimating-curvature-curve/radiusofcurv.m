function [r,a,b]=radiusofcurv(x,y)
% given a load of points, with x,y coordinates, we can estimate the radius
% of curvature by fitting a circle to them using least squares.
  % translate the points to the centre of mass coordinates
  mx = mean(x);
  my = mean(y);
  X = x - mx; Y = y - my; 

  dx2 = mean(X.^2);
  dy2 = mean(Y.^2);

  % Set up linear equation for derivative and solve
  RHS=(X.^2-dx2+Y.^2-dy2)/2; 
  M=[X,Y];
  t = M\RHS;

  % t is the centre of the circle [a0;b0]
  a0 = t(1); b0 = t(2);

  % from which we can get the radius
  r = sqrt(dx2+dy2+a0^2+b0^2); 

  % return to given coordinate system
  a = a0 + mx;
  b = b0 + my; 

