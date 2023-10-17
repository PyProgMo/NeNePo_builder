#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import sys

readspec = 'signal_sum.out'
plotl = [readspec]

def fftspec(data, time):
    spec = np.fft.fft(data)
    freq=np.fft.fftfreq(len(data),d=float(time[1])-float(time[0]))
    spec=abs(spec)[freq>0]
    freq=freq[freq>0]*1.0e5/3.0
    return spec, freq

def gausswin(time, i, dt, data):
    return np.exp(-1e-5*(time-i*dt)**2)*data

def kaiserwin(time, i, data, kwinp = 500, kwinbeta=4.5):#4.5):
    foldd = np.zeros(len(data)+kwinp)
    kwin = np.kaiser(kwinp, kwinbeta)
    for j in range(len(kwin)):
        foldd[j+i] = kwin[j]
    return foldd[int(kwinp/2):-int(kwinp/2)]*data

def normmap(data, norm):
    mapmax = np.max(data)
    print(mapmax)
    return data/mapmax*norm

for i in range(len(plotl)):
    dat = np.loadtxt(plotl[i])
    data = dat[:,1]
    print(len(data))
    time = dat[:,0]
    dt = time[1]-time[0]
    datagfold = []
    datastft = []
    for i in range(len(time)):
        fwinlen = 1000#int(len(data)/2)
        kwinb = 4.5 
        datagfold.append(kaiserwin(time, i, data, kwinp=fwinlen, kwinbeta=kwinb))#gausswin(time, i, dt, data)) kwinbeta=4.5
        specft = fftspec(datagfold[-1], time)[0]
        confwin = np.concatenate((np.zeros(i), np.kaiser(fwinlen, kwinb)*np.max(data), np.zeros(len(time)-i)))[int(fwinlen/2):-int(fwinlen/2)]
        fwin = fftspec(confwin, time)[0]
        datastft.append(np.subtract(specft, fwin))
    fftfreq = fftspec(datagfold[0], time)[1]
    mmin = np.max(datastft)*0.01
    for i in range(len(datastft)):
        for j in range(len(datastft[i])):
            if datastft[i][j] < mmin:
                datastft[i][j] = mmin
    datagfold = normmap(datagfold, 1)
    datastft = normmap(datastft, 1)
    plt.imshow(np.transpose(datagfold), interpolation='nearest', extent=[time[0], time[-1], time[-1], time[0]], aspect='auto', cmap='jet')
    plt.xlabel('time in fs')
    plt.ylabel('max')
    plt.show()
    plt.imshow(np.transpose(datastft)[::-1],  interpolation='nearest', extent=[time[0], time[-1], fftfreq[0], fftfreq[-1]], aspect='auto', cmap='jet')#,  cmap='turbo')
    plt.ylabel('freq in cm⁻¹')
    plt.xlabel('time in fs')
    plt.show()

