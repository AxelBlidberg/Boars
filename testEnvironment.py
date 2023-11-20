from Environment import *

'''
Test file for running tests on the environment program
'''

def PlotFunction(data, limit):
    '''
    Temporary function for plotting the environment. Takes a special formatted list obtained from the ExportContent method in the Environment class.
    '''
    # Divide data
    flowers = []
    for object in data:
        if object[0] == 'flower':
            flowers.append(object)

    nests = []
    for object in data:
        if object[0] == 'Nest':
            nests.append(object)

    types = [item[1] for item in flowers]
    x_values = [item[2] for item in flowers]
    x_NestValues = [item[2] for item in nests]
    y_values = [item[3] for item in flowers]
    y_NestValues = [item[3] for item in nests]

    unique_types = set(types)
    color_map = {t: i for i, t in enumerate(unique_types)}
    colors = [color_map[t] for t in types]

    plt.scatter(x_values, y_values, c=colors, cmap='viridis', s=50, alpha=0.8, label=types)
    plt.scatter(x_NestValues, y_NestValues, marker='^', color='black', label='Black Triangles', s=100)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot with Colors')
    plt.xlim([0, limit])
    plt.ylim([0, limit])
    plt.show()

# Variables
size = 100
flowers = 10
envType = 'urban'
envType = 'agriculture'

env = Environment(size, envType)
env.InitializeFlowers(flowers)
env.InitializeBeeNest(10)
print('Creation distribution: ', env.FlowerDistribution())

for i in range(30):
    obj = np.random.choice(env.flowers)
    env.AddFlower(obj.location, 5, obj.type)

print('Procreation distribution', env.FlowerDistribution())

PlotFunction(env.ExportContent(), size)