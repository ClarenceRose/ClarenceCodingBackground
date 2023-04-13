#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:00:23 2023

@author: lisarose
"""
"""create two subplots in a row, as in the figure below. In both, the x-axis 
extends from - 2 to 2, and the y-axis extends from -2.5 to 2.5. The first 
subplot plots sin(x) (solid blue line) and 2sin(x) (dashed red line) from -2pi 
to 2pi using 40 equally spaced values for x. The second subplot plots cos(x) 
and 2cos(x) similarly. Include legends, and label the x-axis and y-axis as 
shown, sharing the y-axis. Both subplots have a grid and both have the x-axis 
and y-axis drawn as 1-point black lines. Save the figure to file. """

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define x values
x = np.linspace(-2*np.pi, 2*np.pi, 40)

# Define y values for sin(x) and 2sin(x)
y_sin = np.sin(x)
y_2sin = 2 * np.sin(x)

# Define y values for cos(x) and 2cos(x)
y_cos = np.cos(x)
y_2cos = 2 * np.cos(x)

# Set up figure and axes
fig, axs = plt.subplots(1, 2, sharey=True, figsize=(14, 4))
fig.suptitle('Trigonometric Functions', fontsize=16)

# Plot sin(x) and 2sin(x) in the first subplot
axs[0].plot(x, y_sin, 'b-', label=r'$\sin(x)$')
axs[0].plot(x, y_2sin, 'r--', label=r'$2\sin(x)$')
axs[0].set_xlabel('x')
axs[0].set_ylabel('y')
axs[0].set_title('Sine Function')
axs[0].grid(True)
axs[0].spines['left'].set_linewidth(1)
axs[0].spines['bottom'].set_linewidth(1)
blue_patch1 = mpatches.Patch(color='blue', label='sin(x)')
red_patch1 = mpatches.Patch(color='red', label='2 sin(x)')
axs[0].legend(handles=[blue_patch1, red_patch1])

# Plot cos(x) and 2cos(x) in the second subplot
axs[1].plot(x, y_cos, 'b-', label=r'$\cos(x)$')
axs[1].plot(x, y_2cos, 'r--', label=r'$2\cos(x)$')
axs[1].set_xlabel('x')
axs[1].set_title('Cosine Function')
axs[1].grid(True)
axs[1].spines['left'].set_linewidth(1)
axs[1].spines['bottom'].set_linewidth(1)
blue_patch2 = mpatches.Patch(color='blue', label='cos(x)')
red_patch2 = mpatches.Patch(color='red', label='2 cos(x)')
axs[1].legend(handles=[blue_patch2, red_patch2])

# Save figure to file
plt.savefig('trig_functions.png')

# Show the plot
plt.show()
