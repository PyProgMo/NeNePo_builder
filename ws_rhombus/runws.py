#!/usr/bin/env python3
import os

parameters = {'infile1': 'forcean.fchk', 'infile2': 'ani.log', 'temperature': '20', 'ncord': '10'}
os.system('rm *.in')
paras = ['gaussian', 'forcean.fchk', 'ani.log', 20.0, 10, 'dynamics']
os.system('./Wignernointerface.py {} {} {} {} {} {} {}'.format('gaussian', 'forcean.fchk', 'ani.log', 20.0, 10, 'dynamics', None))
