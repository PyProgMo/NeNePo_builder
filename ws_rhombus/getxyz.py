#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gaussian_parser import Checkpoint
import numpy as np
import read_xyz as reader
import os

element_d = {1:'H', 2:'He', 6:'C', 7:'N', 8:'O', 9:'F', 10:'Ne', 47:'Ag'}
ang2au = 0.529177249

cp = Checkpoint('force.fchk')
data = np.multiply(cp.parseCheckpointFile()['_Current_cartesian_coordinates'], ang2au)
print('data =', data)
symbols = cp.parseCheckpointFile()['_Atomic_numbers']

with open("geometry.xyz", "w") as f:
    f.write(str(len(symbols)))
    f.write('\n\n')
    for cord, sym in zip(np.split(data, 4), symbols):
        f.write("{}\t{}\t{}\t{} \n".format(element_d[sym], cord[0], cord[1], cord[2]))
    f.write('\n')
