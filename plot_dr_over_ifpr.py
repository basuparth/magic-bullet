"""
Plot the detection ratio over the inverse false positive rate.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import time

from matplotlib.lines import Line2D
from pathlib import Path


# -----------------------------------------------------------------------------
# MAIN CODE
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    # -------------------------------------------------------------------------
    # Preliminaries
    # -------------------------------------------------------------------------

    print('')
    print('PLOT DETECTION RATIO OVER THE INVERSE FALSE POSITIVE RATE')
    print('')

    # Start the stopwatch
    script_start = time.time()

    # -------------------------------------------------------------------------
    # Create pandas data frame from results and initialize plot
    # -------------------------------------------------------------------------

    # Read in the results as a dataframe and fix some data types
    print('Reading in data...', end=' ', flush=True)
    dataframe = pd.read_json(path_or_buf='./results/dr_over_ifpr.json',
                             orient='records',
                             lines=True)
    dataframe = dataframe.astype({"det_ratio": float,
                                  "fp_rate": float,
                                  "threshold": float,
                                  "window_size": int})
    dataframe['threshold'] = np.around(dataframe['threshold'], decimals=1)
    print('Done!', flush=True)

    # Extract the values for the thresholds and window sizes
    thresholds = sorted(np.unique(dataframe['threshold'].values))
    window_sizes = sorted(np.unique(dataframe['window_size'].values))

    # -------------------------------------------------------------------------
    # Create the parametrized plot
    # -------------------------------------------------------------------------

    # Set up the subplots
    fig, ax = plt.subplots(nrows=1)

    # Define the markers we will be using for the plot (and make it cyclic)
    def markers(index):
        markers_ = ['o', 'v', 'P', 's', 'D', 'x']
        return markers_[index % len(markers_)]

    # Plot a line for every threshold value
    print('Creating plot...', end=' ', flush=True)
    for i, threshold in enumerate(thresholds):

        # Select the line for this threshold value
        line = dataframe[dataframe['threshold'] == threshold]

        # Keep track of all data points on that line
        X, Y = [], []

        # Select datapoints on that line from the dataframe
        for window_size in window_sizes:
            datapoint = line.loc[line['window_size'] == window_size]
            X.append(datapoint['ifp_rate'].values[0])
            Y.append(datapoint['det_ratio'].values[0])

        # Annotate each data point with corresponding the window size
        for x, y, window_size in zip(X, Y, window_sizes):
            ax.plot(x, y, color=f'C{i}', marker=markers(i), ms=3, mew=0.5)
            ax.annotate('{}'.format(window_size), xy=(x, y), xytext=(0, -5.5),
                        ha='center', va='center', textcoords='offset points',
                        fontsize=4.5, color=f'C{i}')
    print('Done!', flush=True)

    # -------------------------------------------------------------------------
    # Set up options for the plot
    # -------------------------------------------------------------------------

    # Set up axes limits
    plt.xlim(3e-1, 6e3)
    plt.ylim(0.82, 0.98)

    # Set up axes scales
    plt.xscale('log')

    # Set up axes labels
    plt.xlabel('Inverse False Positive Rate (s)', fontsize=8)
    plt.ylabel('Detection Ratio', fontsize=8)

    # Put a grid on the plot
    plt.grid(which='both', ls='-', color='#D9D9D9', lw=0.5)

    # Adjust label sizes
    plt.tick_params(axis='both', which='major', labelsize=6)
    plt.tick_params(axis='both', which='minor', labelsize=6)

    # Add a custom legend to the plot
    legend_elements = [Line2D([], [], label=f'Threshold {threshold}',
                              color=f'C{i}', marker=markers(i), ls='None',
                              mew=0.5, ms=3)
                       for i, threshold in enumerate(thresholds)]
    plt.legend(handles=legend_elements, loc='upper right',
               fontsize=6, framealpha=1)

    # Adjust the plot size
    plt.tight_layout()
    width = 8.6 / 2.54 / 1.025
    fig.set_size_inches(width, 2 / 3 * width, forward=True)

    # Construct path for this plot file
    plots_dir = './plots'
    Path(plots_dir).mkdir(exist_ok=True)
    file_path = os.path.join(plots_dir, 'dr_over_ifpr.pdf')

    # Save the plot at the constructed location (as a PDF)
    print('Saving plot as PDF...', end=' ', flush=True)
    plt.savefig(file_path, bbox_inches='tight', pad_inches=0)
    print('Done!', flush=True)

    # -------------------------------------------------------------------------
    # Postliminaries
    # -------------------------------------------------------------------------

    print('')
    print(f'This took {time.time() - script_start:.1f} seconds!')
    print('')
