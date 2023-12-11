import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

from standaloneSimulation import *

#Definition av rum
#Grid på 1000 x 1000
#En pixel är 0.2 x 0.2 m i verkligheten total utsträckning på 1 km

#Definition av tid
#Season lenght = 112000
#Vi räknar med att ett bi max lever 8 veckor
#En dag är 2000 tidssteg

def run_model(size, num_bees=1, num_flowers=20, envType='countryside', NumSeason=1, seasonLength=100, iterations=10):

    beesim = BeeSim(size, num_bees, num_flowers, envType, NumSeason, seasonLength)

    clustering_coefficients = []
    min_radius = 10
    vor = None
    init_positions = np.array([[flower.x, flower.y] for flower in beesim.environment.flowers])
    init_nests = np.array([[nest.x, nest.y] for nest in beesim.environment.nests])
    #vor_init = Voronoi(positions)
    #for _ in range(iterations):
       # beesim.Update()
        # if beesim.timestep % seasonLength ==0:
        #     positions = [(flower.x, flower.y) for flower in beesim.environment.flowers]
        #     vor = Voronoi(positions)
        #     clustering_coefficients.append(clustering(vor, len(beesim.environment.flowers), min_radius))
    beesim.RunSimulation()
    positions = np.array([[flower.x, flower.y] for flower in beesim.environment.flowers])
    nests = np.array([[nest.x, nest.y] for nest in beesim.environment.nests])

    
    #vor = Voronoi(positions)
        
    return init_positions, positions, init_nests, nests #vor_init, vor, clustering_coefficients
        
def clustering(vor, N, min_radius):
    valid_count = 0
    for region in vor.regions:
        if not -1 in region and len(region) > 2:
            polygon_points = vor.vertices[region]
            area = 0.5 * np.abs(np.dot(polygon_points[:, 0], np.roll(polygon_points[:, 1], 1)) - np.dot(np.roll(polygon_points[:, 0], 1), polygon_points[:, 1]))
            if area < np.pi*(min_radius**2):
                valid_count += 1

    clustering_coefficient = valid_count / N
    return clustering_coefficient

def plot_clustering(size, num_bees=1, num_flowers=20, envType='countryside', NumSeason=1, seasonLength=100, iterations=10):

   # vor_init, vor, clustering_coefficients = run_model(size, num_bees, num_flowers, envType, visualize, NumSeason, seasonLength, iterations)

    init_positions, positions, init_nests, nests = run_model(size, num_bees, num_flowers, envType, NumSeason, seasonLength, iterations)

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # Plot Voronoi plot in the first column
    #voronoi_plot_2d(vor_init, ax=axes[0], show_vertices=False, line_colors='lightblue', line_width=2, line_alpha=0.6, point_size=8)
    #print(f"init_positions: {init_positions}")
    #print(f"positions: {positions}")

    axes[0].scatter(init_positions[:,0], init_positions[:,1], marker='.') 
    axes[0].scatter(init_nests[:,0], init_nests[:,1], marker='s', s=25) 
    axes[0].set_title('Initial configuration') 
    axes[0].set_xlim(0, size) 
    axes[0].set_ylim(0, size) 
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    
    # Plot Voronoi plot in the second column
    #voronoi_plot_2d(vor, ax=axes[1], show_vertices=False, line_colors='lightblue', line_width=2, line_alpha=0.6, point_size=8)
    #axes[1].plot(positions)
    axes[1].scatter(positions[:,0], positions[:,1], marker='.') if len(positions)>1 else print("no final flowers")
    
    axes[1].scatter(nests[:,0], nests[:,1], marker='s', s=25) if len(nests>1) else print("no final nests")
    
    axes[1].set_title('Final configuration')
    axes[1].set_xlim(0, size)  
    axes[1].set_ylim(0, size)    
    axes[1].set_xticks([])
    axes[1].set_yticks([])

    #axes[2].plot(clustering_coefficients[:], label='Clustering')
    #axes[2].legend()

    plt.tight_layout()

    plt.show()

size = 1000
seasonLength = 5000
numStartingFlowers = 2000
numStartingBees = 10
NumSeason = 2

iterations = (seasonLength)*NumSeason
plot_clustering(size=1000, num_bees=numStartingBees, num_flowers=numStartingFlowers, envType='countryside', NumSeason=NumSeason, seasonLength=seasonLength, iterations=iterations)