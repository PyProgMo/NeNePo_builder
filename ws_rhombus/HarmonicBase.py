#!/usr/bin/env python

import numpy as np

class HarmonicBase:
    
    autoangs = 0.529177210903
    toaumass = 1822.8884845
    wntohartree = 4.55633528121223e-6

    def __init__(self, nmodes, lowfreq):
        """This is a basis class for handling hessian and normal mode calculations"""
        
        self.nmodes = nmodes
        self.lowfreq = lowfreq

    def readFile(self,filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()

    def setStructure(self):
        pass

    def setMasses(self):
        pass

    def setHessian(self):
        pass
    
    def setMassWeightedHessian(self):
        for i in range(self.ndim):
            for j in range(self.ndim):
                self.hessian[i][j] = self.hessian[i][j]/np.sqrt(self.masses[i]*self.masses[j])
    
    def setTransformationMatrix(self):
        # get eigenvalues (squares of eigenfrequencies) and eigenvectors
        # of mass weighted hessian. lmat is transformation matrix between 
        # mass weighted coordinates and mass weighted normal coordinates
        eigv = np.linalg.eig(self.hessian)
        self.ind = np.argsort(eigv[0])
        self.lmat = np.zeros((self.ndim, self.ndim))
        # print(eigv[0])
        # for i in range(self.ndim):
        #     print eigv[1].T[i][self.ndim-1]
        for i in range(self.ndim):
            for j in range(self.ndim):
                # compared to Numeric, indices of eigenvector are interchanged, 
                # hence the transpose
                self.lmat[i][j] = eigv[1].T[self.ind[i]][j]
        # normal frequencies for translation and rotation have to be exactly 0
        self.normfreq = np.sort(eigv[0])

        # Cut selected frequencies.
        if self.lowfreq is None:
            if self.nmodes is None:
                # All modes are selected, except for translations and rotations.
                # Linearity will be determined automatically.
                p = self.coordinates.reshape(-1, 3)
                p0 = np.average(p, axis=0)
                u, s, v = np.linalg.svd(p - p0)
                if s[1]/s[0] < 0.01:
                    print('Linear molecule!')
                    m = 5
                else:
                    print('Nonlinear molecule!')
                    m = 6
            else:
                # First `nmodes` modes will be cut.
                m = self.nmodes
        else:
            # Regardless of `nmodes`, modes with frequencies upto lowfreq
            # will be cut.
            eigval_max = (self.lowfreq*self.wntohartree)**2
            m = np.asarray(self.normfreq < eigval_max).nonzero()[0][-1] + 1

        self.nmodes = m

        self.normfreq[:m] = 0.0
        if self.normfreq.min() < 0.0:
            print('WARNING: Imaginary frequencie(s) detected!')
        self.normfreq = np.sqrt(self.normfreq)
        
        print('{} modes cut!'.format(m))
        print('First used mode: {} cm^{{-1}}.'.format(self.normfreq[m]/self.wntohartree))

    def getTransformationMatrix(self):
        return self.lmat

    def getNormalFrequencies(self):
        return self.normfreq

    def getHessian(self):
        return self.hessian

    def getCoordinates(self):
        return self.coordinates

    def getSymbols(self):
        return self.sym

    def getMasses(self):
        return self.masses
