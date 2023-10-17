#!/usr/bin/env python3
import numpy as np
import os, sys
import matplotlib.pyplot as plt

opflss = 'Traj_'
opflse = '.out'
au2ev = 27.211324570273
os.system('mkdir ipevalu')

files = os.listdir()
ipfile = 'rhombus_Energy.out'
data = [] # contains all ips and times [time, ip]
# time in fs, ip in eV
writedata = [['ipevalu/scf_neutral_fs_eV.txt', 1, 1], ['ipevalu/scf_cation_fs_eV.txt', 2, 1], ['ipevalu/all_ips_fs_eV.txt', 3, au2ev]]

def writeip(data):
    for h in range(len(writedata)):
        with open(writedata[h][0], 'w') as f:
            for i in range(len(data[0][0])):
                f.write('{0}\t'.format(data[0][0][i]))
                for j in range(len(data)):
                    f.write('{0}\t'.format(data[j][h+1][i]))
                f.write('\n')

for i in files:
    if opflss in i and opflse in i:
        ipl = [[]]
        try:
            dat = np.loadtxt('{0}/{1}'.format(i, ipfile))
            #print(dat)
            ipl[0]=dat[:,0]
            for j in writedata:
                ipl.append(np.multiply(dat[:,j[1]], j[2]))
        except:
            print('Error by loading data')
        data.append(ipl)

writeip(data)
