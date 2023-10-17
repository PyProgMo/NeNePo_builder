#!/usr/bin/env python

import numpy as np
import os
from HarmonicBase import HarmonicBase

class HarmonicGaussian(HarmonicBase):
    def __init__(self, nmodes, lowfreq, filename1, filename2):
        """This is a class handling Gaussian hessian and normal mode calculations"""
        super().__init__(nmodes, lowfreq)
        self.readFile(filename1)
        self.suffix = os.path.splitext(filename1)[-1].replace('.', '')
        self.filename2 = filename2

    def setStructure(self):
        with open(self.filename2, "r") as f:
            lines = f.readlines()
            self.setStructureLog(lines)

    def setStructureLog(self, lines):
        flag = 0
        self.sym = []
        for i in range(2, len(lines) - 1):
            if flag == 1:
                self.sym.append(lines[i].split(",")[0])
                if len(lines[i + 1].split(",")) != 5:
                    flag = 0
            if "Redundant internal coordinates found in file" in lines[i]:
                flag = 1
            if "Input orientation" in lines[i]:
                startind = i
        flag = 1
        self.coordinates = []
        for i in range(startind + 5, len(lines)):
            if "-------------" in lines[i]:
                flag = 0
            if flag == 1:
                h = lines[i].split()
                self.coordinates.append(float(h[3])/self.autoangs)
                self.coordinates.append(float(h[4])/self.autoangs)
                self.coordinates.append(float(h[5])/self.autoangs)
        self.coordinates = np.array(self.coordinates)
        print(np.array(self.coordinates)*0.5291772)
        self.ndim = len(self.coordinates)
        self.nat = self.ndim//3

    def setStructureChk(self):
        flag = 0
        with open(self.filename2, 'r') as f:
            li = f.readlines()
        self.sym = []
        for i in range(2, len(li) - 1):
            if flag == 1:
                self.sym.append(li[i].split()[0])
                if len(li[i + 1].split()) != 4:
                    flag = 0
            if "Symbolic Z-matrix" in li[i - 1]:
                flag = 1

        flag = 0
        self.coordinates = []
        for i in range(len(self.lines)):
            #if ("Opt point" in self.lines[i])and ("Gradient" in self.lines[i]):
            if "Force Field"in self.lines[i]:
                flag = 0
            if flag == 1:
                h = self.lines[i].split()
                for j in range(len(h)):
                    self.coordinates.append(float(h[j]))
            #if ("Opt point" in self.lines[i])and ("Geometries" in self.lines[i]):
            if "Current cartesian coordinates"in self.lines[i]:
                flag = 1
        self.coordinates = np.array(self.coordinates)
        self.ndim = len(self.coordinates)
        self.nat = self.ndim//3

    def setMasses(self):
        if self.filename2 == "":
            # this option if everything is read from a log file
            li = self.lines
        else:
            # this option if hessian is read from fchk file, the file here should then be the log file
            with open(self.filename2, 'r') as f:
                li = f.readlines()
        
        self.masses = []
        for i in range(len(li)):
            if ("has atomic number" in li[i]) and ("and mass" in li[i]):
                self.masses.append(self.toaumass*float(li[i].split()[8]))
                self.masses.append(self.toaumass*float(li[i].split()[8]))
                self.masses.append(self.toaumass*float(li[i].split()[8]))
        self.masses = np.array(self.masses)

    def setHessian(self):
        if self.suffix == "fchk":
            self.setHessianChk()
        else:
            self.setHessianLog()

    def setHessianLog(self):
        self.hessian = np.zeros((self.ndim, self.ndim))

        # reading hessian from Gaussian output
        for i in range(len(self.lines)):
            if "Force constants in Cartesian coordinates:" in self.lines[i]:
                ind1 = i
            if "Force constants in internal coordinates:" in self.lines[i]:
                ind2 = i
        flag = 0
        for i in range(ind1 + 1, ind2):
            h = self.lines[i].split()
            if (len(h) == 5) and (flag == 0):
                hessind2 = np.array(list(map(int, h))) - 1
                flag = 1
            else:
                hessind1 = int(h[0]) - 1
                for ii in range(1, len(h)):
                    self.hessian[hessind1][hessind2[ii - 1]] = float(h[ii].replace("D", "E"))
                    self.hessian[hessind2[ii - 1]][hessind1] = self.hessian[hessind1][hessind2[ii-1]]
                if (len(h) == 6) and (len(self.lines[i + 1].split()) == 5):
                    flag = 0

    def setHessianChk(self):
        self.hessian = np.zeros((self.ndim, self.ndim))

        for i in range(len(self.lines)):
            if "Cartesian Force Constants" in self.lines[i]:
                startind = i + 1
        endind = startind + (self.ndim*self.ndim + self.ndim)//10
        # only only half the force constant matrix is printed in fchk file
        # (N**2-N)/2+N = (N**2+N)/2 distinct values, arranged in 5 columns per line
        # if this number cannot be divided by 5, one incomplete line has to be added
        if ((self.ndim**2 + self.ndim)//2)%5 != 0:
            endind += 1
        h = []
        for i in range(startind, endind):
            h.append(list(map(float, self.lines[i].split())))
        count = 0
        for i in range(self.ndim):
            for j in range(i + 1):
                zeile = count//5
                spalte = count%5
                self.hessian[i][j] = h[zeile][spalte]
                self.hessian[j][i] = self.hessian[i][j]
                count += 1
