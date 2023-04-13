#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:20:27 2023

@author: lisarose
"""
"""Read in this file and form a sum of each of the four kinds of fruit. 
Suppose that these numbers are in list cnts in the same order as the columns 
(i.e., apples, oranges, pears,bananas). From these numbers, you produce the 
pie chart"""
import matplotlib.pyplot as plt

# Read in the contents of the fruits.txt file
with open('fruits.txt') as f:
    data = f.readlines()

# Parse the data to get the counts for each type of fruit
cnts = [0, 0, 0, 0]
for line in data:
    nums = line.strip().split()
    for i in range(4):
        cnts[i] += int(nums[i])

# Create the pie chart
labels = ['Apples', 'Oranges', 'Pears', 'Bananas']
explode = [0.1, 0, 0, 0]
fig1, ax1 = plt.subplots()
ax1.pie(cnts, explode=explode, labels=labels, autopct='%.1f%%', shadow=True)
ax1.set_title('Fruit Counts')

# Save the figure to a file
plt.savefig('fruit_counts_pie_chart.png')

# Show the plot
plt.show()
