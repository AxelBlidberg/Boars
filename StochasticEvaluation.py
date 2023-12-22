import copy, pickle

def CopySimulation(blueprint, n):
    '''
    Returns n copies of the blueprint simulation.
    '''
    simulations = [copy.deepcopy(blueprint) for i in range(n)]
    print(f'\n{n} copies of the simulation created.\n')
    return simulations

def SaveSimulation(filename, data):
    '''
    Saves the simulation file under the filename specified.
    '''
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    print(f'\nSimulation saved as {filename}\n')

def LoadSimulation(filename, n=1):
    '''
    Loads the simulation file under the filename specified and returns the specified number of copies.
    '''
    if n == 1:
        # Load one simulation
        with open(filename, 'rb') as file:
            simulation = pickle.load(file)
        print(f'\nSimulation loaded from {filename}\n')
        return simulation
    else:
        # Load one simulation and return n copies of the same simulation
        simulations = []
        with open(filename, 'rb') as file:
            simulation = pickle.load(file)
            for _ in range(n):
                simulations.append(copy.deepcopy(simulation))
        print(f'\n{n} simulations loaded from {filename}.\n')
        return simulations
