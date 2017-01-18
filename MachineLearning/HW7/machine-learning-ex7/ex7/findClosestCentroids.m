function idx = findClosestCentroids(X, centroids)
%FINDCLOSESTCENTROIDS computes the centroid memberships for every example
%   idx = FINDCLOSESTCENTROIDS (X, centroids) returns the closest centroids
%   in idx for a dataset X where each row is a single example. idx = m x 1 
%   vector of centroid assignments (i.e. each entry in range [1..K])
%

% Set K
K = size(centroids, 1);

% You need to return the following variables correctly.
idx = zeros(size(X,1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Go over every example, find its closest centroid, and store
%               the index inside idx at the appropriate location.
%               Concretely, idx(i) should contain the index of the centroid
%               closest to example i. Hence, it should be a value in the 
%               range 1..K
%
% Note: You can use a for-loop over the examples to compute this.
%

distance = zeros(size(X,1),K);

    
    
    
for j = 1:size(centroids)
        
    
    
    diffs = bsxfun(@minus, X, centroids(j,:))
    
    distance(:,j)=(sum(diffs.^2,2))
        
        %dif = X(i)-centroids(j);
        %sqr_dif = dif * dif;
        
        %if sqr_dif <= min
           
       %     min = sqr_dif;
       %     cen_loc = j;
            
        %end
        
end
    

for i = 1:size(X,1)
   [minvalue, index_of_min] = min(distance(i,:));
   
   
   idx(i) = index_of_min;
   
end
   


    
    






% =============================================================



