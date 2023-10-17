#!/usr/bin/env python

import numpy as np

class WignerEnsemble:

    def __init__(self, interface, temp, ncond, fname):
        self.interface = interface
        self.temp = temp
        self.ncond = ncond
        self.interface.setStructure()
        self.interface.setMasses()
        self.interface.setHessian()
        self.interface.setMassWeightedHessian()
        self.interface.setTransformationMatrix()
        self.ndim = len(self.interface.getCoordinates())
        self.nat = self.ndim//3
        self.nzerofreq = self.interface.nmodes
        self.autoangs = interface.autoangs
        self.fname = fname

    def initialConditions(self,i):
        if self.temp < 1e-16:
            A = 1.0
        else:
            A = np.tanh(1.0*self.interface.getNormalFrequencies()[i]/(2.0*3.1671e-6*self.temp))
        dq = np.sqrt(1.0/(2.0*self.interface.getNormalFrequencies()[i]*A))
        dp = np.sqrt(1.0*self.interface.getNormalFrequencies()[i]/(2.0*A))
        q0 = np.random.normal(0.0, dq)
        p0 = np.random.normal(0.0, dp)
        return q0, p0

    def getWignerEnsemble(self):
        self.invmassmatrix = np.array([np.zeros(self.ndim) for j in range(self.ndim)])
        for i in range(self.ndim):
            self.invmassmatrix[i][i] = 1.0/np.sqrt(self.interface.getMasses()[i])

        c0 = self.interface.getCoordinates()
        # lmat = inverse(self.interface.getTransformationMatrix())
        lmat = np.transpose(self.interface.getTransformationMatrix())

        with open("allstruct.xyz", "w") as allout:
            for ii in range(self.ncond):
                q = []
                p = []
                for j in range(self.ndim):
                    if j < self.nzerofreq:
                        q0 = 0.0
                        p0 = 0.0
                    else:
                        q0, p0 = self.initialConditions(j)
                    q.append(q0)
                    p.append(p0)
                q = np.array(q)
                p = np.array(p)
                c = np.dot(self.invmassmatrix, np.dot(lmat, q))
                vel = np.dot(self.invmassmatrix, np.dot(lmat, p))
                coord = c + c0
                with open(self.fname + "_" + '{:04d}'.format(ii) + ".in", "w") as f:
                    f.write(str(self.nat) + "\n")
                    allout.write(str(self.nat) + "\n")
                    allout.write("\n")
                    for i in range(self.nat):
                        f.write("{0:s} {1[0]:20.14f} {1[1]:20.14f} {1[2]:20.14f}\n"\
                                .format(self.interface.getSymbols()[i], coord[3*i:3*i + 3]))
                        allout.write("{0:s} {1[0]:20.14f} {1[1]:20.14f} {1[2]:20.14f}\n"\
                                .format(self.interface.getSymbols()[i], coord[3*i:3*i + 3]*self.autoangs))
                    for i in range(self.nat):
                        f.write("{0[0]:20.14f} {0[1]:20.14f} {0[2]:20.14f}\n".format(vel[3*i:3*i + 3]))
