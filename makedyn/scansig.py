#!/usr/bin/env python3
import os, sys, shutil, subprocess
import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from scipy.interpolate import interp1d
import scipy.constants as const

head_end = '.out'
target = 'Average_signal_out'
savesig = 'signal_map_sum.out'
savefftsig = 'signal_fft_sum.out'
plot_script = 'showspec.py'
pfad = os.getcwd()
Eprobel=np.arange(4.0, 6.7, 0.2)#5.9, 6.3, 0.02) E_probe in eV
hbar = 0.6582119569 # eV * fs
fs2au = 41.341374575751
ev2au = 0.036749405469679
E_pu=1.59#*ev2au [eV] old=1.59
sigma_pu=80#*fs2au [fs]
sigma_pr=5#40#50#*fs2au [fs]

def Signal1(t, td): # all units in [fs]
    return np.exp(-(t-td)**2/(sigma_pu**2+sigma_pr**2))
def Signal2(ip, E_pr):
    if E_pr > ip:
        sig2 = 1
    else:
        sig2 = np.exp(-(sigma_pr**2)/(hbar**2)*(E_pr-ip)**2)
    return sig2
def Signal3(E_vde):
    if E_pu > E_vde:
        sig3 = 1
    else:
        sig3 = np.exp(-(sigma_pu**2)/(hbar**2)*(E_pu-E_vde)**2)
    return sig3
def sig1_sig2(t, td, ip, E_pr):
    return float(Signal1(t, td)*Signal2(ip, E_pr))

def getspec(time_delays, Energy, E_pr):
    data = np.loadtxt(Energy)
    E_ip = np.multiply(data[:, 3], 1/ev2au)
    try:
        E_vde=np.loadtxt("vde.out")/ev2au
    except:
        E_vde=1

    interval=200#*fs2au calc is already in fs
    Vip = interp1d(time_delays, E_ip, kind='cubic')
    os.system('truncate -s 0 signal.out')
    signal=int_new(time_delays, E_ip, E_vde, Vip, interval, E_pr)#, delta_t)
    return signal

def int_new(time_delays, E_ip, E_vde, Vip, interval, E_pr, onespec=False):#, delta_t):
    result3 = 1#Signal3(E_vde)
    complsig= []
    for td, ip in zip(time_delays, Vip(time_delays)):
        times = [td-interval, td+interval]
        #sig = integrate.quad(sig1_sig2, times[0], times[-1], args=(td, ip))[0]*result3
        sig = sig1_sig2(np.arange(times[0], times[1], 2*interval), td, ip, E_pr)*result3
        # write signal in signal.out if only one spectrum is calculated
        if onespec == True:
            os.system("echo {}\t{} >> signal.out".format(td, sig))
        complsig.append(sig)
    return complsig

def getdynargs(filen, dtc, nstepc):
    look=True
    dynste=None
    deltat=None
    with open(filen) as f:
        data = f.readlines()
    i  = 0
    while look == True:
        if dtc in data[i]:
            deltat = int(data[i].split(' ')[0].split('=')[-1])
        elif nstepc in data[i]:
            dynste = int(data[i].split(' ')[0].split('=')[-1])
        if dynste==None or deltat==None:
            i +=1
        else:
            look = False
    return deltat, dynste

def readin_std(name):
    time = []
    sig = []
    with open(name) as f:
        data = f.readlines()
        for i in data:
            s = i.split(' ')
            time.append(float(s[0]))
            sig.append(float(s[1].split('\n')[0]))
    return time, sig

def getfl(ending):
    files = os.listdir()
    filel = []
    for i in files:
        if ending in i:
            filel.append(i)
    return filel

def col_spec(files, E_pr):
    os.chdir(files)
    datan = getspec(times, getfl('_Energy.out')[0], E_pr)
    os.chdir(pfad)
    return(datan)

try:
    os.system('./remnonedyns.py')
except:
    print('Error while running remnonedyns.py')

tstep, dynl = getdynargs('zekecalc.sub', 'deltat', 'dynste') #read tstep and dynl from subfile
times=np.arange(0, dynl*tstep+tstep, tstep)

outfiles = getfl(head_end)
#generate spectra for different Laser energies
data = []

def fftspec(data, time):
    spec = np.fft.fft(data)
    freq=np.fft.fftfreq(len(data),d=float(time[1])-float(time[0]))
    spec=abs(spec)[freq>0]
    freq=freq[freq>0]*1.0e13/const.c
    return spec, freq


def writematrix(filename, data, times, scan):
    with open(filename, 'w') as f:
        f.write('0')
        for i in scan:
            f.write('\t{}'.format(i))
        f.write('\n')
        for i in range(len(data)):
            f.write('{}'.format(times[i]))
            for j in range(len(data[i])):
                f.write('\t{}'.format(data[i][j]))
            f.write('\n')

for k in Eprobel:
    os.chdir(pfad)
    datan = Parallel(n_jobs=-1)(delayed(col_spec)(outfiles[i], k) for i in range(len(outfiles)))
    data = np.append(data, np.einsum('ij->j', datan))
    #del datan

data = np.reshape(data, (len(Eprobel), len(times)))

fftdata = []
fftdat, fftfreqs = fftspec(data[0], times)
fftdata.append(fftdat)
for i in range(len(data)-1):
   fftdata.append(fftspec(data[i+1], times)[0])

fftdata = np.transpose(fftdata)
data = np.transpose(data)
os.chdir(target)

os.system('truncate -s 0 {}'.format(savesig))
writematrix(savesig, data, times, Eprobel)
writematrix(savefftsig, fftdata, fftfreqs, Eprobel)
os.system('./{}'.format(plot_script))
