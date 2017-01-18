X = [1 1;1 2; 1 3];

y = [1;2;3];

theta = [0;0];

predictions = X*theta

sqrErrors = (predictions - y) .^2

sum(sqrErrors)/(2*length(y))
