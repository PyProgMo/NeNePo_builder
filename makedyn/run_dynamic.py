#!/usr/bin/env python3
# enable Berensen Thermostat manuel in VV_X.py
from VV_8_4 import VelocityVerlet
import os, sys
import numpy as np
import catscfsp2 as cat

filename = ['rhombus', 'Ag4'] # Name of Job and Name of .com-file
write = 2 # write -flag
iteration = int(sys.argv[1]) #20 # Anzahl der Interationsschritte
dt = float(sys.argv[2]) # dt in fs
tau = 80.0 # fs
T = 20 # T-soll in K
Thermostate = False
Tempr = [tau, T, Thermostate]
initfile = cat.get_in('.in')
method=['gaussian', 'Total']

ensemble = VelocityVerlet(dt, iteration, filename, write, Tempr, initfile, method)
ensemble.simulate()
cat.calcat('{}_dynamics.xyz'.format(filename[0]), '{}cat'.format(filename[1]), 'neut_stru.xyz', 'forcecat', '{}_Energy.out'.format(filename[0]))

# get vde
cat.anic(cat.get_in('_dynamics.xyz'), free=1) # init for Anion calc
os.system('g16 Ag4ani.com Ag4ani.log')
os.system('formchk forcean.chk forcean.fchk')
cat.get_ip('forcean.fchk', cat.get_in('_Energy.out'))
