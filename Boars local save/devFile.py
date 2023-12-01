import numpy as np
import matplotlib.pyplot as plt

def InitializeFlowers(limit, n):
    nRows = int(np.sqrt(n))
    nCols = int(np.sqrt(n))

    x = np.linspace(10, limit-10, num=nRows)
    y = np.linspace(10, limit-10, num=nCols)
    flowers = [[i, j] for i in x for j in y]
    for line in flowers:
        print(line)
    

    return flowers

def PlotFunction(nodes):
    x = [i[0] for i in nodes]
    y = [i[1] for i in nodes]

    for i in range(len(x)):
        plt.scatter(x[i], y[i])

    plt.show()

flowers = InitializeFlowers(1000, 100)
PlotFunction(flowers)

