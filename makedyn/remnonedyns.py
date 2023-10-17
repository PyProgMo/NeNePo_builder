#!/usr/bin/env python3
import sys, os

path = os.getcwd()
def get_in(ending):
    files = os.listdir()
    il = []
    for i in files:
        if ending in i:
            il.append(i)
    return il

os.system('mkdir dynerror')
outs = get_in('.out')
for i in outs:
    os.chdir(i)
    error = False
    ensc = get_in('_Energy.out')
    if len(ensc) > 0:
        for j in ensc:
            with open(j) as f:
                data = f.readlines()
                for k in data:
                    if 'None' in k:
                        error = True
    os.chdir(path)
    #os.system('cd {0}'.format(path))
    if error == True:
        os.system('mv {0} dynerror/.'.format(i))
