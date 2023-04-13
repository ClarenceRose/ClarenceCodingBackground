#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:11:50 2023

@author: lisarose
"""
"""Generate a list of 1000 numbers from a normal distribution 
(see np.random.normal()) with x = 2 and x = 0.5 and plot them in a step-style 
histogram (use histtype='step') with 50 bins as shown in the figure below. 
Rotate the x-axis tick labels 45 degrees as shown (rotation=45). Include the 
y label and title shown. Save the figure to file."""

import numpy as np
import matplotlib.pyplot as plt

# Generate 1000 random numbers from a normal distribution with mean 2 and standard deviation 0.5
mu, sigma = 2, 0.5
data = np.random.normal(mu, sigma, 1000)

# Plot the data in a step-style histogram with 50 bins
plt.hist(data, bins=50, histtype='step')

# Set the x-axis and y-axis labels and title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Normal Distribution Histogram')

# Rotate the x-axis tick labels by 45 degrees
plt.xticks(rotation=45)

# Save the figure to file
plt.savefig('normal_distribution_histogram.png')

# Show the plot
plt.show()
