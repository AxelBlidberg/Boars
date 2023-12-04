from newSimulation import *

beesim = BeeSimulation(500, 2, 150)



for i in range(10000):
    beesim.Update()