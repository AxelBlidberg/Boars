import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create a DataFrame with sample data
df = pd.DataFrame(np.random.randn(100, 3), columns=['A', 'B', 'C'])

# Create a Matplotlib subplot layout
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Plot the box plot created with Pandas on the first subplot
box_plot_ax = df.boxplot(ax=axs[0])
axs[0].set_title('Box Plot using Pandas')

# Plot another subplot (for comparison or additional plots)
axs[1].scatter(np.random.randn(100), np.random.randn(100))
axs[1].set_title('Another Subplot')

# Show the entire subplot layout
plt.show()