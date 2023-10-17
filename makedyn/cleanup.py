#!/usr/bin/env python3
import numpy as np
import os, sys
import matplotlib.pyplot as plt

pfad = os.getcwd()

def getout(name=['Traj_', '.out']):
    dirl = []
    for i in os.listdir():
        if name[0] in i and name[1] in i and '.swp' not in i:
            dirl.append(i)
    return dirl

def readtemptxt():
    clean = False
    read = {}
    try:
        with open('temp.txt', 'r') as f:
            data = f.readlines()
        for i in range(len(data)):
            slidt = data[i].split('\n')[0].split('=')
            read.update({slidt[0].strip(' '):slidt[1].strip(' ')})
    except:
        pass
    read = tempcheckvalue(read, 'cleaned')
    return read

def writetemptxt(read):
    a = list(read.keys())
    b = list(read.values())
    with open('temp.txt', 'w') as f:
        for i in range(len(a)):
            f.write('{}={}\n'.format(a[i], b[i]))

def tempcheckvalue(read, value):
    try:
        a = read[value]
    except:
        read.update({value:'False'})
    return read

def cleanup(clean):
    if clean['cleaned'] == 'False' or clean['cleaned'] == 'false':
        try: 
            os.system('mkdir collectslurm')
        except:
            pass
        try: 
            os.system('mkdir input')
        except:
            pass
        os.system('mv *.out collectslurm/.')
        os.system('mv Traj_* input/.')
        os.system('mv collectslurm/Traj_* .')
        clean['cleaned']='True'
    return clean

def checkstability(fl1, fl2):
    os.chdir(pfad)
    dirl = getout()
    stabil = []
    escf = []
    temper = []
    for i in dirl:
        os.chdir('{}/{}'.format(pfad, i))
        os.system('rm -r Gau*') #removes remaining Gau* files
        escf.append(np.loadtxt(getout([fl1[0], ''])[0])[:,fl1[1]])
        temper.append(np.loadtxt(getout([fl2[0], ''])[0])[:,fl2[1]])
        stabil = np.add(escf, temper)
        plt.plot(stabil[-1], label='stabil')
        plt.plot(escf[-1], label='scf')
        plt.plot(temper[-1]+np.max(escf[-1]), label='temperatur')
        plt.legend()
        plt.show()

rdata = readtemptxt()
rdata = cleanup(rdata)
writetemptxt(rdata)
checkstability(['_Energy.out', 1],['_dipol_moment.out', 5])
