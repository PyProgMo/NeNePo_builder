#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os, sys


openend='.txt'
ev2hatree = 0.0367493

#print(len(data), len(data[0]))
def plotdata(data, show, name):
    # plot each IP seperately
    #for i in range(len(data[0])-1):
    #    plt.plot(data[:, 0], data[:, i+1])
    #plt.xlabel('time in fs')
    #plt.show()
    
    #plot only averaged IP
    if show == True:
        if 'ips' in name:
            plt.plot(data[:, 0], np.einsum('ij->i', data[:,1:]/(len(data[0])-1)), label=name)
        else:
            plt.plot(data[:, 0], np.einsum('ij->i', data[:,1:]/(len(data[0])-1)), label=name)
            plt.yticks([])
    else: 
        if 'ips' in name:
            pld = np.einsum('ij->i', data[:,1:]/(len(data[0])-1))*ev2hatree
            plt.plot(data[:, 0], np.add(pld, -1*np.amin(pld)), label=name)
        else:
            pld = np.einsum('ij->i', data[:,1:]/(len(data[0])-1))
            plt.plot(data[:, 0], np.add(pld, -1*np.amin(pld)), label=name)
        #plt.yticks([])
    plt.legend()
    plt.xlabel('time in fs')
    plt.ylabel('oszillating Averaged ensemble IP')
    if show == True:
        plt.show()

def fftspec(data, time):
    spec = np.fft.fft(data)
    freq=np.fft.fftfreq(len(data),d=(float(time[1])-float(time[0])))
    spec=abs(spec)[freq>0]
    freq=freq[freq>0]*1.0e5/3.0
    return spec/np.max(spec), freq

def plotfftspecs(data):
    ffts = []
    fftsum =[[], []]
    for i in range(len(data[0])-1):
        ffts.append(fftspec(data[:, i+1], data[:, 0]))
    fftsum[0] = ffts[0][1]#freqs
    fftsum[1] = np.zeros(len(ffts[0][0]))

    #plot each fft-IP seperately
    for i in range(len(ffts)):
        fftsum[1] += ffts[i][0]
    #    plt.plot(ffts[i][1], ffts[i][0])
    #plt.show()
    
    #plot the averaged fft-IP of the whole ensemble
    plt.plot(fftsum[0], fftsum[1])
    plt.xlabel('freq in cm⁻¹')
    plt.ylabel('fft amplitude')
    plt.yticks([])
    plt.show()

alldata = []
names = []
for i in os.listdir():
    if openend in i:
        names.append(i)
        with open(i) as f:
            data = np.loadtxt(f)
            alldata.append(data)
        print(i)
        plotdata(data, True, i.split('.')[0]) # plot IPs
        plotfftspecs(data) # fft IPs

for j in range(len(alldata)):
    plotdata(alldata[j], False, names[j].split('.')[0])
plt.show()

