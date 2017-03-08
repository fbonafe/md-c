###Real Time Plotting in python - Example ###

import numpy as np
import matplotlib.pyplot as plt

plt.axis([0,100,0,10000])
plt.ion()

for i in range(100):
	y = i**2
	z = i**3
    # y = np.random.random()
	plt.scatter(i,y)
	plt.scatter(i,z)
	plt.pause(0.05)

while True:
    plt.pause(0.05)
