import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

def calculate_accuracy(tp, fp, tn, fn):
    return (tp + tn) / (tp + tn + fp + fn)

def plot_accuracy(json_file, distortion_method, hashing_method):
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Extract the relevant data
    method_data = data[distortion_method][hashing_method]
    
    # Prepare data for plotting
    phash_thresholds = []
    dhash_thresholds = []
    accuracies = []

    for threshold_pair, values in method_data.items():
        # Parse the string formatted thresholds
        phash_threshold, dhash_threshold = map(float, threshold_pair.strip('()').split(', '))
        tp, fp, tn, fn = values
        accuracy = calculate_accuracy(tp, fp, tn, fn)
        phash_thresholds.append(phash_threshold)
        dhash_thresholds.append(dhash_threshold)
        accuracies.append(accuracy)
    
    # Convert lists to numpy arrays
    phash_thresholds = np.array(phash_thresholds)
    dhash_thresholds = np.array(dhash_thresholds)
    accuracies = np.array(accuracies)
    
    # Create a finer grid for interpolation
    phash_grid_fine, dhash_grid_fine = np.meshgrid(
        np.linspace(phash_thresholds.min(), phash_thresholds.max(), 100),
        np.linspace(dhash_thresholds.min(), dhash_thresholds.max(), 100)
    )
    
    # Interpolate the accuracy values over the finer grid
    accuracy_grid_fine = griddata(
        (phash_thresholds, dhash_thresholds),
        accuracies,
        (phash_grid_fine, dhash_grid_fine),
        method='cubic'
    )

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the surface
    surf = ax.plot_surface(phash_grid_fine, dhash_grid_fine, accuracy_grid_fine, cmap='viridis')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    ax.set_xlabel('PHash Threshold')
    ax.set_ylabel('DHash Threshold')
    ax.set_zlabel('Accuracy')
    ax.set_title(f'Accuracy vs Thresholds for {distortion_method} and {hashing_method}')
    
    # Save plot to file
    plt.savefig(f'assets/results/50K Phash-Dhash-Phash_Dhash_Vit/{distortion_method}_{hashing_method}_accuracy.png')


# Example usage
json_file = 'assets/results/50K Phash-Dhash-Phash_Dhash_Vit/optimal_thresholds_values.json'
distortion_method = 'blur-2'
hashing_method = 'Phash_Dhash'
plot_accuracy(json_file, distortion_method, hashing_method)