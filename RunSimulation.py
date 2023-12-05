from newSimulation import *

#Definition av rum
#Grid på 1000 x 1000
#En pixel är 0.2 x 0.2 m i verkligheten total utsträckning på 1 km

#Definition av tid
#Season lenght = 112000
#Vi räknar med att ett bi max lever 8 veckor
#En dag är 2000 tidssteg


beesim = BeeSimulation(1000, 3, 2000,112000)

mean_egg = [0,0]

n_days = 10

for i in range(2000*n_days):
    beesim.Update()

    if i % 2000 == 0 and i > 0:
        distribution_result = beesim.swarm.distribution
        #print(distribution_result)
        #print(beesim.swarm.total_egg)
        if distribution_result[0] > 0:
            mean_egg[0] += beesim.swarm.total_egg[0]/(distribution_result[0])
        
        if distribution_result[1] > 0:
            mean_egg[1] += beesim.swarm.total_egg[1]/(distribution_result[1])


print(mean_egg[0]/n_days)
print(mean_egg[1]/n_days)

