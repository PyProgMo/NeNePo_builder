#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import scipy.constants as const

openend='.txt'

#print(len(data), len(data[0]))
def plotdata(data):
    for i in range(len(data[0])-1):
        plt.plot(data[:, 0], data[:, i+1])
    plt.show()

def fftspec(data, time):
    spec = np.fft.fft(data)
    freq=np.fft.fftfreq(len(data),d=(float(time[1])-float(time[0])))
    spec=abs(spec)[freq>0]
    freq=freq[freq>0]*1.0e13/const.c
    return spec, freq

def plotfftspecs(data):
    ffts = []
    fftsum =[[], []]
    for i in range(len(data[0])-1):
        ffts.append(fftspec(data[:, i+1], data[:, 0]))
    fftsum[0] = ffts[0][1]#freqs
    fftsum[1] = np.zeros(len(ffts[0][0]))
    for i in range(len(ffts)):
        fftsum[1] += ffts[i][0]
        plt.plot(ffts[i][1], ffts[i][0])
    plt.show()

    plt.plot(fftsum[0], fftsum[1])
    plt.show()

for i in os.listdir():
    if openend in i:
        with open(i) as f:
            data = np.loadtxt(f)

        plotdata(data) # plot IPs
        plotfftspecs(data) # fft IPs

