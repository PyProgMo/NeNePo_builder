#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.constants as const

readspec = 'signal_sum.out'
plotl = [readspec]

def fftspec(data, time):
    spec = np.fft.fft(data)
    freq=np.fft.fftfreq(len(data),d=float(time[1])-float(time[0]))
    spec=abs(spec)[freq>0]
    freq=freq[freq>0]*1.0e13/const.c
    return spec, freq

for i in range(len(plotl)):
    dat = np.loadtxt(plotl[i])
    data = dat[:,1]
    time = dat[:,0]
    dt = time[1]-time[0]
    datagfold = []
    datastft = []
    for i in range(len(time)):
        datagfold.append(np.exp(-1e-5*(time-i*dt)**2)*data)
        datastft.append(np.subtract(fftspec(datagfold[-1], time)[0], fftspec(np.exp(-1e-5*(time-i*dt)**2)*np.max(data), time)[0]))
    fftfreq = fftspec(datagfold[0], time)[1]
    mmin = np.max(datastft)*0.01
    for i in range(len(datastft)):
        for j in range(len(datastft[i])):
            if datastft[i][j] < mmin:
                datastft[i][j] = mmin
    plt.imshow(datagfold, interpolation='nearest', extent=[time[0], time[-1], time[0], time[-1]])
    plt.show()
    plt.imshow(datastft,  interpolation='nearest', extent=[fftfreq[0], fftfreq[-1], time[0], time[-1]])#,  cmap='turbo')
    plt.show()


