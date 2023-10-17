#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits import mplot3d
import sys, os

dataf = 'signal_map_sum.out'
dataft = 'signal_fft_sum.out'
plotl = [[dataf, True], [dataft, False]]

for i in range(len(plotl)):
    data = np.loadtxt(plotl[i][0])
    Elaser= np.around(data[0, 1:], decimals=7)
    yaxis= data[1:, 0]
    data = np.transpose(data[1:,1:])
    #if plotl[i][1] == True:
    #    data = np.flip(np.transpose(data[1:, 1:]))
    plt.ylabel('Laser [mEv]')
    if 'fft' in plotl[i][0]:
        plt.xlabel('freq in cm-1')
    else:
        plt.xlabel('time in fs')
    plt.imshow(data, interpolation='nearest', extent=[yaxis[0], yaxis[-1], Elaser[-1]*1000, Elaser[0]*1000], aspect='auto', cmap='jet')
    plt.show()

