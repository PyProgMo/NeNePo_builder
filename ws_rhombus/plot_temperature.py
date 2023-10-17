#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os

geoms = []
names = []
for i in sorted(os.listdir()): 
    if '.in' in i and os.path.isfile(i):
        geoms.append(i)
        names.append(os.path.splitext(i)[0].split('_')[-1])

m_dict = {'h': 1.00784, 'c': 12.0107, 'ag':107.8682}

Temperatures = []
for g, n in zip(geoms, names):
    masses = []
    velocities = []
    with open(g, 'r') as f: 
        for line in f: 
            temp = line.split()
            if len(temp) == 4: 
                masses.append(m_dict[temp[0].lower()])
            elif len(temp) == 3: 
                velocities.append([float(x) for x in temp[0:]])

    masses = np.array(masses) * 1822.888486
    velocities = np.array(velocities)
    
    Ekin = np.sum(0.5*masses*np.sum(velocities**2, axis=1))
    T = (2*Ekin*27.2114)/(3*len(masses)*8.617333262e-5)
    print('{}: Ekin = {} a.u., Temp = {} K'.format(n, Ekin, T))
    Temperatures.append(T)
    
    # Ekin = 0.5*masses*np.sum(velocities**2, axis=1)
    # T = (2*Ekin*27.2114)/(3*8.617333262e-5)
    # Temperatures.extend(T)

Temperatures = np.array(Temperatures)

plt.hist(Temperatures, bins=10*int(np.log10(len(Temperatures))))
plt.show()

