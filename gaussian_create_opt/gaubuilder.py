#!/usr/bin/env python3
import os, sys
import optionsan as o

stdir = os.getcwd()

# copy .com file, basis and .xyz file in target
def copycalcdata():
    os.chdir(stdir)
    os.system('cp {}/{}.xyz {}/{}/{}.coord'.format(o.xyzinput, o.xyzinpname, o.sdir, o.name, o.coord))
    os.system('cp {}/{} {}/{}/basis'.format(o.basisdir, o.basis, o.sdir, o.name))

#build com files from o:
def buildcoms():
    os.chdir(stdir)
    os.chdir('{}/{}'.format(o.sdir, o.name))
    with open('{}.com'.format(o.comfile), 'w') as f:
        f.write('%Nproc={}\n'.format(o.cores))
        f.write('%Mem={}Mb\n'.format(o.memory*960))
        f.write('%chk={}.chk\n'.format(o.checkfile))
        f.write('{}\n\n'.format(o.inputline))
        f.write('{}\n\n'.format(o.comments))
        f.write('{} {}\n'.format(o.charge, o.multi))
        f.write('@{}.coord\n\n@basis\n\n'.format(o.coord))

def wrinp():
    os.chdir(o.lib)
    with open(o.rawsubscr, 'r') as f:
        data = f.readlines()
    for i in range(len(o.inpl)):
        for j in range(len(data)):
            if 'inp{}'.format(i) in data[j]:
                data[j] = data[j].replace('inp{}'.format(i), str(o.inpl[i]))         
    os.chdir(stdir)
    os.chdir(o.sdir)
    with open(o.subscr, 'w') as f:
        for i in data:
            f.write(i)
    os.system('chmod +x {}'.format(o.subscr))

# create folder
os.system('mkdir {}'.format(o.sdir))
os.system('mkdir {}/{}'.format(o.sdir, o.name))
# copy and create files

wrinp()
copycalcdata()
buildcoms()
