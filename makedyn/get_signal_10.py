#!/usr/bin/env python3
import numpy as np
import os,sys,time,subprocess
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.integrate as integrate

fs2au = 41.341374575751
ev2au = 0.036749405469679
hbar = 0.6582119569 # eV * fs
E_pu=1.59#*ev2au [eV] old=1.59
E_pr=3.15*2#*ev2au  [eV]
sigma_pu=80#*fs2au [fs]
sigma_pr=50#*fs2au [fs]

def Signal1(t, td): # all units in [fs]
    return np.exp(-(t-td)**2/(sigma_pu**2+sigma_pr**2))
def Signal2(ip):
    return np.exp(-(sigma_pr**2)/(hbar**2)*(E_pr-ip)**2)
def Signal3(E_vde):
    return np.exp(-(sigma_pr**2)/(hbar**2)*(E_pu-E_vde)**2)
def sig1_sig2(t, td, ip):
    return Signal1(t, td)*Signal2(ip)
def getspec(time_delays, Energy):
    data = np.loadtxt(Energy)
    E_ip = np.multiply(data[:, 3], 1/ev2au)
    try:
        E_vde=np.loadtxt("vde.out")/ev2au
    except: 
        E_vde=1

    interval=200#*fs2au calc is already in fs
    Vip = interp1d(time_delays, E_ip, kind='cubic')
    os.system('truncate -s 0 signal.out')
    int_new(time_delays, E_ip, E_vde, Vip, interval)#, delta_t)

def int_new(time_delays, E_ip, E_vde, Vip, interval):#, delta_t):
    result3 = Signal3(E_vde)
    for td, ip in zip(time_delays, Vip(time_delays)): 
        times = [td-interval, td+interval]
        sig = integrate.quad(sig1_sig2, times[0], times[-1], args=(td, ip))[0]*result3
        os.system("echo {}\t{} >> signal.out".format(td, sig))             
