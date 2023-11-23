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

    plt.scatter(x_values, y_values, c=colors, cmap='viridis', s=10, alpha=0.8, label=types)
    plt.scatter(x_NestValues, y_NestValues, marker='^', color='black', label='Black Triangles', s=20)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot with Colors')
    plt.xlim([0, limit])
    plt.ylim([0, limit])
    plt.show()

def AddFlowers(n):
    for i in range(n):
        obj = np.random.choice(env.flowers)
        env.AddFlower(obj.location, 5, obj.type)

def AddNests(n):
    for i in range(n):
        obj = np.random.choice(env.nests)
        env.AddBeeNest(obj.location, 5)


# Variables
size = 1000
flowers = 100
nests = 30
envType1 = 'urban'
envType2 = 'agriculture'

env = Environment(size)
env.InitializeFlowers(flowers)
env.InitializeBeeNest(nests)
print('\n > Creation distribution:        ', env.FlowerDistribution())
print(len(env.flowers))

AddFlowers(30)
AddNests(10)
#env.PushUpdate()

print(' > Procreation distribution:     ', env.FlowerDistribution())
print(len(env.flowers))

PlotFunction(env.ExportContent(), size)