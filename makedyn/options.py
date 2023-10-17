#!/usr/bin/env python3
# Author: Moritz Limbacher 23.06.2023
# set options for bilder.py to build dynamic in ../septraj/ dir
# needs wiegner sampled ensemble

#Wigner Sampler Options:            # samppath/wsinpfiles/wsinput1
samppath    = '../ws_rhombus/.'     # path of Wigner Sampler
wsinpfiles  = 'TPSSh_tzvp'              # path of opt struct inside samppath
qchemmethod = 'gaussian'
wsinput1    = 'forcean.fchk'        # ws input name inside wsinpfiles
wsinput2    = 'ani.log'
temperature = 30                   # WS Temperature in K
wsoutfile   = 'dynamics'            # name of .in files
wsfile      = 'Wignernointerface.py'
trajnum     = 1000               # number n of trajectories, numbering begins with 0 to n-1

#ensemble dynamicsname = nameXXXX.in with 4 digits for numbering
ensname     = 'dynamics'
ensdir      = '../ws_rhombus'      #init structs must be found here
enstarg     = '../septraj'          #target directory
states      = ['an', 'neut', 'cat'] #observing states
multineut   = 'T'                   #multiplicity of second state

# gaussian com files for states
comdir      = 'comfiles/'           # dir of .com files
comnames    = {'an': 'Ag4ani.com', 'neut': 'Ag4.com', 'cat': 'Ag4cat.com'} 
nproc       = 4                    # nproc per task
mempercpu   = 3                     # mem per cpu in Gb for slurm
usenproc    = '%Nproc={}\n'.format(nproc) # n proc for gaussian
mem         = '%Mem={}Mb\n'.format(int(nproc*mempercpu*960)) # mem per calc for gaussian in Mb
chkln       = {                     # name of fchk files
            'an':'%chk=forcean.chk\n', 
            'neut':'%chk=force.chk\n', 
            'cat':'%chk=forcecat.chk\n'}
qchem_meth  = 'TPSSh'               # method
gaussianinp = {                     # input line for gaussian depending on states
            'an': '#P {} GENECP symmetry=None stable=opt Guess(Read,TCheck)\n'.format(qchem_meth),
            'neut':'#P force {} GENECP symmetry=None Guess(Read,TCheck)\n'.format(qchem_meth),
            'cat': '#P {} GENECP symmetry=None Guess(Read,TCheck)\n'.format(qchem_meth)}
comments    = 'Comments\n'
mult_charge = {                     # charge and multiplicity of states
            'an': '-1 2\n',
            'neutS': '0 1\n',
            'neutT': '0 3\n',
            'cat': '+1 2\n',}
struct      = {'an':'coord.xyz\n',      # coord.xyz = init .xyz file
            'neut': 'temp.xyz\n',       # temp.xyz = propagated by VV
            'cat': 'neut_stru.xyz\n'}   # calced along neutral neut .xyz trajectory
# which basis to use? filename = basdir/basname+basend
# basisname is the name of the basis for the calculation
basname     = 'def2-tzvp'
basend      = '.1.gbs'
basdir      = 'basisdir'
basisname   = 'basis'

# build input
run_dyn_scr = 'run_dynamic.py'  # init and run VelocityVerlet
dynstname   = 'dynstart.bash'   # script to submit job array
steps       = 1               # number n of steps to be done leads to n+1 points
dt          = 5                 # time step delta t in [fs]
rawsubscr   = 'zekecalcraw'     # raw sub script
subscr      = 'zekecalc.sub'    # submission script
inpl        = [nproc, mempercpu, steps, dt]
