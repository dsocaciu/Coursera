a2 = zeros(3,1)
x = ones(3,1)

Theta1 = [1,2,3;4,5,6;7,8,9]

for i = 1:3
    for j = 1:3
        a2(i) = a2(i) + x(j) * Theta1(i,j);
    end
    a2(i)=sigmoid(a2(i));
end

a2