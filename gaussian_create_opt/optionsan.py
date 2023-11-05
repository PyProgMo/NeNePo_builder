#!/usr/bin/env python3

# mkdir input
name = 'UCCSD'                                # name of optimisation
rawsubscr = 'rawsub'                        # name .sub file
lib = 'lib'                                 # place scripts here
basisdir = 'basisdir'                       # place all basis files here
xyzinput = 'xyzinput'                       # place .xyz files here
xyzinpname = 'neut_init'                    # name of .xyz input file  !!! without .xyz ending !!!
sdir = 'optgaussian'                           # subdir
subscr = '{}.sub'.format(name)              # name of .sub file
#scripts = ['gaussian_parser.py', 'getxyz.py', 'read_xyz.py'] # scripts in /bin

# gaussian calculation input
qchem = 'gaussian'                          # qchem method
comfile = 'optstruct'                       # name of comfile !!! without .com ending !!!
cores = 40                                  # number of cores
memory = 3                                  # memory per core in Gb
checkfile = 'force'                       # fchk file name  !!! without .fchk ending !!!
method = 'UCCSD'                            # qchem method
inputline = '#P opt {} GENECP freq'.format(method) # input line
comments = 'freq for triangle'              # comments
charge = -1                                 # charge
multi = 2                                   # multiplicity
coord = 'init'                            # .coord file !!! wothout .coord ending !!!
basis = 'def2-tzvp.1.gbs'                   # basis file

inpl = [cores, memory, name, comfile, checkfile]
