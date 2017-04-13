'''
Fruit weight estimation
'''

import numpy as np
import random
import matplotlib.pyplot as plt

# Number of fruits
n = 500

# generate n random numbers from 0 to 9
a = np.random.randint(10, size=n)

# weight of grapefruits is centered around 160g
grapefruits = 160 + a - np.mean(a)

# weight of oranges is centered around 96g
a = np.random.randint(10, size=n)
oranges = 96 + a - np.mean(a)

# aggregate grapefruits and oranges int list
fruits = list(oranges) + list(grapefruits)

# randomize
fruits = random.sample(fruits , len(fruits) )

# average weight of all fruits
fruits_mean_weight = np.mean(fruits)
# initialize estimated threshold
estimated_threshold = 100
# Memorize the thresholds at each iteration for plotting
thresholds = []


k = 1
# Loop over all fruits
for f in fruits:
    # update the threshold
    estimated_threshold = (k*estimated_threshold + f)/ (k+1)
    # memorize thresholds
    thresholds.append(estimated_threshold)
    k = k+1

# plot
fig, ax = plt.subplots(1,1, figsize=(6,6))

ax = plt.subplot(1,1,1)
ax.set_axis_bgcolor('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# The thresholds iteration after iteration
plt.plot(thresholds)
# The target true value: average weight of all fruits
plt.hlines(fruits_mean_weight + 2, 1, 2* n, linestyles='dashed', color = 'red')

