#!/usr/bin/env python3

import sys
import importlib

from WignerBase import WignerEnsemble

qc_programmes = {
        '1': 'molpro',
        '2': 'gaussian',
        '3': 'turbomole',
        '4': 'mndo',
        '5': 'bagel',
        }

if len(sys.argv) == 1:
    # Initialisation of WignerEnsemble class
    #
    # 1) HarmonicInterface according to the quantum chemistry program used.
    #    Interface is initialised with flag for linear/nonlinear molecule (0/1)
    #    and by providing names of input files
    #    - MOLPRO: Standard output of frequency calculation
    #    - GAUSSIAN: (i) formatted checkpoint file + standard outputfile
    #                (ii) [AT THE MOMENT THIS DOES NOT WORK] only standard outputfile (second filename should be "")
    #    - TURBOMOLE: aoforce outputfile, "coord" file
    #    - MNDO: Standard output of frequency calculation, "molden.dat" file
    # 2) Temperature in K
    # 3) Number of initial conditions to be generated
    # 4) Name string of ouputfiles (e.g. "dynamics" or "structure")
    
    # Specify the quantum chemistry programme
    qcp_input = input(
            'Please specify the quantum chemistry programme you used for the frequency calculation.\n'
          + 'Currently supported programmes are:\n'
          + '(1) Molpro\n'
          + '(2) Gaussian\n'
          + '(3) Turbomole\n'
          + '(4) MNDO\n'
          + '(5) BAGEL\n')
    try:
        qcp_idx = int(qcp_input)
    except ValueError:
        qcp = qcp_input.strip().lower()
    else:
        qcp = qc_programmes[str(qcp_idx)]
    
    # Provide data
    print()
    if qcp == 'molpro':
        infile1 = input('Please provide the standard output file of frequency calculation.\n')
        infile2 = ''
    elif qcp == 'gaussian':
        infile1 = input('Please provide the formatted checkpoint file\n')
        infile2 = input('and the standard outputfile.\n')
    elif qcp == 'turbomole':
        infile1 = input('Please provide the aoforce outputfile\n')
        infile2 = input('and the "coord" file.\n')
    elif qcp == 'mndo':
        infile1 = input('Please provide the standard output file from frequency calculation\n')
        infile2 = input('and the "molden.dat" file.\n')
    elif qcp == 'bagel':
        infile1 = input('Please provide the standard output file of frequency calculation.\n')
        infile2 = ''
    else:
        raise RuntimeError('The programme {} is currently not supported!'.format(qcp))

    infile1 = infile1.strip()
    infile2 = infile2.strip()
    
    # Specify number of modes to be cut
    print()
    mc_inp = input('How may modes would you like to discard? Type in\n'
                 + '  1 to specify the number of modes you like to discard and\n'
                 + '  2 to specify the lowest frequency in cm^{-1} you want to keep.\n'
                 + 'Any other input will result in keeping all modes except for translations and rotations,\n'
                 + 'equivalent to select `1` and specify 5 for linear and 6 for non-linear molecules.\n')
    mc_inp = mc_inp.strip()
    if mc_inp == '1':
        print()
        nmodes = input('How many modes would you like to discard?\n'
                     + 'This number should be at least 5 for linear molecules\n'
                     + 'and 6 for non-linear molecules.\n')
        nmodes = int(nmodes)
        lowfreq = None
    elif mc_inp == '2':
        print()
        lowfreq = input('What is the lowest frequency you want to keep (in cm^{-1})?\n')
        lowfreq = float(lowfreq)
        nmodes = None
    else:
        nmodes = None
        lowfreq = None
        print('`nmodes` will be selected automatically.')

    # Specify the temperature
    print()
    temperature = input('At what temperature should the structures be sampled? (in K)\n')
    temperature = float(temperature)

    # Specify the number of initial conditions
    print()
    ncond = int(input('How many initial conditions do you want to generate?\n'))

    # Specify the prefix of output initial conditions
    print()
    outfile = input('Please specify the name string of output files.\n'
                  + '(e.g. "dynamics" or "structure")\n').strip()

elif len(sys.argv) == 2:
    import toml
    
    parameters = toml.load(sys.argv[1])['parameters']
    qcp = parameters['qcp'].lower()
    infile1 = parameters['infile1'].strip()
    infile2 = parameters.get('infile2', '').strip()
    temperature = float(parameters['temperature'])
    ncond = int(parameters['ncond'])
    outfile = parameters['outfile'].strip()
    
    nmodes = parameters.get('nmodes', None)
    lowfreq = parameters.get('lowfreq', None)

else:
    print('USAGE')

# Load harmonic interface
module_name = 'Harmonic' + qcp.capitalize()
HarmonicModule = importlib.import_module(module_name)
HarmonicInterface = getattr(HarmonicModule, module_name)

we = WignerEnsemble(HarmonicInterface(nmodes, lowfreq, infile1, infile2), temperature, ncond, outfile)
we.getWignerEnsemble()
