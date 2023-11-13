# Just a program to test individual functions

import numpy as np

Euclidan = lambda x1, x2: np.sqrt(sum([(x1[i] - x2[i])**2 for i in range(len(x1))]))
Euclidan2 = lambda x1, x2: np.sqrt((x1[0]-x2[0])**2 + (x1[1] - x2[0])**2)

p1 = [1, 1]
p2 = [5, 5]

print(Euclidan(p1, p2))
print(Euclidan2(p1, p2))