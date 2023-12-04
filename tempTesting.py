from newSimulation import *

sim = BeeSimulation(1000, 20, 500)

counter = 0

while counter < 10**4:
    counter += 1
    sim.Update()