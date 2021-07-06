from math import comb
n = int(input('N: '))

print('Probablity of 1 fake')
prob1 = 1/n * 100
print(prob1)
print('Probability of 2 fake')
prob2 = (3/(n-1))* 100
print(prob2)
print('Probability of 3 fake')
prob3 = ((2*comb(n-3,2))/comb(n,4))* 100
print(prob3)