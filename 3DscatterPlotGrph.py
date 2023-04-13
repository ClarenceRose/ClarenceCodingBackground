#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:32:59 2023

@author: lisarose
"""
"""The first three values are x, y, and z coordinates, and the next value is
the radius. Each line specifies an extended ‘dot’ in a 3D scatter plot at
the given coordinates with the given radius. If the ‘dot’ is given on
data1.txt, it appears as a cyan right-pointing triangle, while if it is
given on data2.txt, it appears as a black left-pointing triangle. The
area is computedas pir2 eventhoughthe‘dot’is a triangle.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def plot_data(filename, ax, marker, color):
    data = np.loadtxt(filename)
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    r = np.pi * data[:, 3] ** 2
    ax.scatter(x, y, z, s=r, marker=marker, color=color)

fig = plt.figure()
ax = plt.axes(projection="3d")

plot_data('data1.txt', ax, '>', 'c')
plot_data('data2.txt', ax, '<', 'k')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title('3D Scatter Plot')

plt.savefig('scatter_plot.png')
