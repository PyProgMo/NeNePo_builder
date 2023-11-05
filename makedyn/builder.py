#!/usr/bin/env python3
import os, sys, shutil
import numpy as np
import options as o

#run ws
def wsinit():
    os.chdir(sdir)
    os.chdir(o.ensdir)
    os.system('rm *.in')
    os.system('./{} {} {} {} {} {} {} {}'.format(o.wsfile, o.qchemmethod, '{}/{}'.format(o.wsinpfiles, o.wsinput1), '{}/{}'.format(o.wsinpfiles, o.wsinput2), o.temperature, o.trajnum, o.wsoutfile, None))
    os.chdir(sdir)
    os.chdir(o.enstarg)
    os.system('rm -r *')
    os.chdir(sdir)

#write data into dynstart.bash
def wrdynstart():
    with open(o.dynstname, 'w') as f:
        f.write('#!/bin/bash\n\n')
        f.write('sbatch --array=0-{}%{} zekecalc.sub\n'.format(o.trajnum-1, o.trajnum))
        f.write('mkdir collectslurm\n')

# write subscript with Info for slurm
# for i element n replace inpi with variable inpi
def wrzekecalc():
    os.chdir(sdir)
    with open(o.rawsubscr, 'r') as f:
        data = f.readlines()
    inpc = 0
    line = 0
    readrawsub = True
    while readrawsub == True:
        if data[line][:3] == 'inp':
            rep = data[line][4:].index('inp')
            data[line] = '{}{}{}'.format(data[line][4:rep+4], o.inpl[int(data[line][rep+7])], data[line][rep+8:])
        line += 1
        if line > len(data)-2:
            readrawsub = False
    os.chdir(o.enstarg)
    with open(o.subscr, 'w') as f:
        for i in data:
            f.write(i)
    os.system('chmod +x {}'.format(o.subscr))
    os.chdir(sdir)

#build com files from o:
def buildcoms():
    for i in o.states:
        os.chdir(o.comdir)
        os.system('touch {}'.format(o.comnames[i]))
        with open(o.comnames[i], 'w') as f:
            f.write(o.usenproc)
            f.write(o.mem)
            f.write(o.chkln[i])
            f.write(o.gaussianinp[i])
            f.write('\n{}\n'.format(o.comments))
            if i == 'neut':
                mult = '{}{}'.format(i, o.multineut)
            else:
                mult = i
            f.write(o.mult_charge[mult])
            f.write('@{}\n'.format(o.struct[i]))
            f.write('@{}\n\n'.format(o.basisname))

        os.chdir(sdir)

sdir=os.getcwd()
wsinit()
buildcoms()
wrdynstart()
os.system('cp {}/* .'.format(o.comdir))

sdf = []
for i in o.states:
    sdf.append(o.comnames[i])
sdf.append(o.run_dyn_scr)

# copy all files into the directory 
cdf = ['average_signal_11.py', 'dynstart.bash', 'get_signal_10.py', 'remnonedyns.py', 'cleanup.py', 'scansig.py', 'average_signal_fast.py', 'plotallIPs2.py']

ending = '.in'
trajends = []
for i in range(o.trajnum):
    trajends.append(str(i))

# create folder and copy all files into Average_signal_out/
avout = ['generate_plot_freqs.py', 'showspec.py', 'stftsigmap2.py', 'kaiserstft1.py']
os.system('mkdir {}/Average_signal_out'.format(o.enstarg))
for i in avout:
    os.system('cp {} {}/Average_signal_out/.'.format(i, o.enstarg))

# create folder and copy all into ipevalue/ 
ipev = ['plotips.py', 'evplotips.py', 'evplotips1.py']
os.system('mkdir {}/ipevalu'.format(o.enstarg))
for i in ipev:
    os.system('cp {} {}/ipevalu/.'.format(i, o.enstarg))

for i in cdf:
    os.system('cp {} {}/.'.format(i, o.enstarg))

wrzekecalc()

for i in trajends:
    curtdir = '{}/Traj_{}'.format(o.enstarg, i)
    infile = 'dynamics_{}{}'.format(str(i).zfill(4), ending)
    os.mkdir(curtdir)
    for j in sdf:
        os.system('cp {0} {1}/.'.format(j, curtdir))
        shutil.copyfile('{}/{}'.format(sdir, j), '{}/{}'.format(curtdir, j))
    shutil.copyfile('{}/{}'.format(sdir, '{}/{}{}'.format(o.basdir, o.basname, o.basend)), '{}/{}'.format(curtdir, o.basisname))
    os.system('cp {0}/{1} {2}/{1}'.format(o.ensdir, infile, curtdir))
