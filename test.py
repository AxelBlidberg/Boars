# Just a program to test individual functions

import matplotlib.pyplot as plt

def plot_points_with_colors(data):
    """
    Plot points from a list of lists with specified colors based on the 'type' field.

    Parameters:
        data (list of lists): List of [class, type, x, y] data points.
    """
    # Extract data for plotting
    classes = [item[0] for item in data]
    types = [item[1] for item in data]
    x_values = [item[2] for item in data]
    y_values = [item[3] for item in data]

    # Create a color map based on unique 'type' values
    unique_types = set(types)
    color_map = {t: i for i, t in enumerate(unique_types)}
    colors = [color_map[t] for t in types]

    # Scatter plot with colors based on 'type'
    plt.scatter(x_values, y_values, c=colors, cmap='viridis', s=50, alpha=0.8, label=types)

    # Add legend based on 'type'
    handles = [plt.Line2D([0], [0], marker='o', color='w', label=t, 
                         markerfacecolor=plt.cm.viridis(color_map[t]), markersize=10) for t in unique_types]
    plt.legend(handles=handles, title='Type')

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot with Colors')
    plt.show()

# Example usage:
data = [
    ['A', 'Type1', 2, 3],
    ['B', 'Type2', 4, 5],
    ['C', 'Type1', 1, 2],
    ['A', 'Type2', 3, 4],
    ['B', 'Type1', 5, 6],
]

plot_points_with_colors(data)
