#!/usr/bin/env python
"""
 Python parser for Gaussian

 author: j.hoche
"""

# imports
import numpy as np
import os
import sys

# global constants
HARTREE_TO_EV = 27.211396132
ANGS_TO_BOHR = 1.0 / 0.52917721092


class Gaussian:
    """
    Interface to Gaussian 16 for TD-DFT calculations.

    Attributes
    ----------
    natoms  : number of atoms of the molecule
    symbols : atomic symbols of the molecule
    coords  : atomic xyz-coordinates of the molecule (Angstrom)
    """

    def __init__(self, filename):
        """
        Inits the Gaussian class.

        Parameters
        ----------
        filename: Name of the input xyz-geometry (in Angs.)

        """
        self.filename = filename
        self.coords = []
        self.symbols = []
        self._read_xyz()

    @staticmethod
    def run_g16(g16_command="g16", com_filename="g16.com", state1_chk="s0.chk", state2_chk="s1.chk"):
        """Run Gaussian16: It requires the availability of the g16 command"""
        os.system("{g16_command} {com_filename}")
        os.system("formchk {state1_chk} > /dev/null")
        os.system("formchk {state2_chk} > /dev/null")
        os.system("rm {state1_chk}")
        os.system("rm {state2_chk}")

    @staticmethod
    def read_results(filename, read_nac=False):
        """Read the energy, gradient (and nonadiabatic couplings
        from the formatted checkpoint file"""
        checkpoint = Checkpoint(filename)
        data = checkpoint.parseCheckpointFile()
        energy = data["_Total_Energy"]
        gradient = data["_Cartesian_Gradient"]
        os.system("rm {filename}")
        if read_nac:
            nac = data["_Nonadiabatic_coupling"]
            return energy, gradient, nac
        # The optimization algorithm seems to work with any random vector
        # that is not parallel to the gradient.
        nac = np.ones(len(gradient))
        return energy, gradient, nac

    def _read_xyz(self):
        """Read the inital geometry file"""
        with open(self.filename, "r") as f:
            self.natoms = int(f.readline())
            for line in f.readlines()[1:]:
                tmp = line.split()
                if len(tmp) >= 4:
                    self.symbols.append(tmp[0])
                    self.coords.append(tmp[1:4])
        self.coords = np.array(self.coords, dtype=float)

    def write_structure(self):
        """Write the new geometry for the Gaussian input"""
        with open("geometry.xyz", "w") as f:
            for s, c in zip(self.symbols, self.coords):
                f.write("%s %12.8f %12.8f %12.8f \n" % (s, c[0], c[1], c[2]))

    def write_xyz(self):
        """Append the actual geometry to the opt.xyz file in a
        trajectory format"""
        with open("opt.xyz", "a") as f:
            f.write(str(self.natoms) + "\n\n")
            for s, c in zip(self.symbols, self.coords):
                f.write("%s %12.8f %12.8f %12.8f \n" % (s, c[0], c[1], c[2]))


class Checkpoint:
    """
    read formatted G09/G16 checkpoint files

    Attributes:
    -----------
    filename : the filename of the Gaussian fchk file
    """
    def __init__(self, filename):
        """
        Inits the Checkpoint class
        """
        assert isinstance(filename, str), "the filename must be a string"
        self.filename = filename

    @staticmethod
    def read_float_block(fh, n):
        """
        read a block of N floats separated into 5 columns
        """
        nrow = n // 5
        if n % 5 != 0:
            nrow += 1
        data = []
        for _ in range(0, nrow):
            line = fh.readline().replace("D", "E")
            parts = line.strip().split()
            data += map(float, parts)
        assert len(data) == n
        return np.array(data, dtype=float)

    @staticmethod
    def read_int_block(fh, n):
        """
        read a block of N integers separated into 6 columns
        """
        nrow = n // 6
        if n % 6 != 0:
            nrow += 1
        data = []
        for _ in range(0, nrow):
            line = fh.readline()
            parts = line.strip().split()
            data += map(int, parts)
        assert len(data) == n
        return np.array(data, dtype=int)

    @staticmethod
    def read_char_block(fh, n):
        """
        read a block of N lines of characters
        """
        data = ""
        for _ in range(0, n):
            line = fh.readline()
            data += line + "\n"
        return data

    def parseCheckpointFile(self, convert=True):
        """A dictonary containing all the blocks read."""
        data = {}
        with open(self.filename, "r") as fh:
            block = _IgnoreBlock([], fh)
            while True:
                line = fh.readline()
                if line == "":
                    # end of file
                    break
                if line[0].isupper() and len(line.split()) > 1:
                    # A capital letter starts a block of information.
                    # The name of the block is used to find the correct
                    # derived class (by appending _Block).
                    block_type, arguments = get_block_type_args(line)
                    try:
                        block = eval(block_type + "_Block")(arguments, fh)
                        # call the constructor of a class that bears the same name
                        # as the current block
                        data[block.get_name()] = block
                    except NameError:
                        block = _IgnoreBlock(arguments, fh)
        py_data = {}
        if convert:
            # convert blocks into a repr. that can be used with python
            for (block_type, block) in data.items():
                py_data[block_type] = block.get_py()
            return py_data
        else:
            return data


def read_float_block(fh, n):
    """
    read a block of N floats separated into 5 columns
    """
    nrow = n // 5
    if n % 5 != 0:
        nrow += 1
    data = []
    for _ in range(0, nrow):
        line = fh.readline().replace("D", "E")
        parts = line.strip().split()
        data += map(float, parts)
    assert len(data) == n
    return np.array(data, dtype=float)


def read_int_block(fh, n):
    """
    read a block of N integers separated into 6 columns
    """
    nrow = n // 6
    if n % 6 != 0:
        nrow += 1
    data = []
    for _ in range(0, nrow):
        line = fh.readline()
        parts = line.strip().split()
        data += map(int, parts)
    assert len(data) == n
    return np.array(data, dtype=int)


def read_char_block(fh, n):
    """
    read a block of N lines of characters
    """
    data = ""
    for _ in range(0, n):
        line = fh.readline()
        data += line + "\n"
    return data


def get_block_type_args(line):
    parts = line.split(" ")
    block_type = ""
    for ip, p in enumerate(parts):
        if p == "":
            arguments = " ".join(parts[ip:]).split()
            break
        else:
            block_type += "_" + p
    # replace reserved characters
    block_type = (
        block_type.replace("-", "_")
        .replace("=", "_")
        .replace(")", "_")
        .replace("(", "_")
        .replace("/", "_")
        .replace("*", "_")
    )
    return block_type, arguments


class _Block:
    def __init__(self, _arguments, _fh):
        return None

    def get_name(self):
        return self.__class__.__name__.replace("_Block", "")

    def get_py(self):
        """returns a representation that can be used with python"""
        return None


class _IgnoreBlock(_Block):
    pass


class single_int_Block(_Block):
    def __init__(self, arguments, _fh):
        assert arguments[0] == "I"
        self.integer = int(arguments[1])

    def get_py(self):
        return self.integer


class _Number_of_atoms_Block(single_int_Block):
    pass


class _Charge_Block(single_int_Block):
    pass


class int_Block(_Block):
    def __init__(self, arguments, fh):
        assert arguments[0] == "I"
        n = int(arguments[2])
        self.data = read_int_block(fh, n)

    def get_py(self):
        return self.data


class float_Block(_Block):
    def __init__(self, arguments, fh):
        assert arguments[0] == "R"
        n = int(arguments[2])
        self.data = read_float_block(fh, n)

    def get_py(self):
        return self.data


class char_Block(_Block):
    def __init__(self, arguments, fh):
        assert arguments[0] == "C"
        n = int(arguments[2])
        self.data = read_char_block(fh, n)

    def get_py(self):
        return self.data


##########################################


class _Atomic_numbers_Block(int_Block):
    pass


class _Nuclear_charges_Block(float_Block):
    pass


class _Int_Atom_Types_Block(int_Block):
    pass


class _MM_charges_Block(float_Block):
    pass


class _Current_cartesian_coordinates_Block(float_Block):
    pass


class _Mulliken_Charges_Block(float_Block):
    pass


class _Cartesian_Gradient_Block(float_Block):
    def get_py(self):
        return self.data


class _Cartesian_Force_Constants_Block(float_Block):
    def get_py(self):
        # Hessian contains lower triangular matrix
        # with N*(N+1)/2 entries where N=Nat*3
        M = len(self.data)
        N = int(0.5 * (np.sqrt(1.0 + 8.0 * M) - 1.0))
        Nat = int(N / 3.0)
        assert (3 * Nat) * (3 * Nat + 1) / 2 == M

        Hess = np.zeros((N, N))
        for j in range(1, N + 1):
            for i in range(1, j + 1):
                indx = (j - 1) * j // 2 + i - 1
                hij = self.data[indx]
                Hess[i - 1, j - 1] = hij
                # hessian is symmetric
                Hess[j - 1, i - 1] = Hess[i - 1, j - 1]
        return Hess


class _Dipole_Moment_Block(float_Block):
    pass


class _Dipole_Derivatives_Block(float_Block):
    pass

class _Nonadiabatic_coupling_Block(float_Block):
    pass

###########################################

class _Number_of_Normal_Modes_Block(single_int_Block):
    pass

class _Vib_E2_Block(float_Block):
    pass

class _Real_atomic_weights_Block(float_Block):
    def __init__(self, arguments, fh):
        super().__init__(arguments, fh)
        self.data = self.data * 1822.88848492937

class _Cartesian_Forces_Block(float_Block):
    pass

class _Dipole_Data_Block(float_Block):
    pass

###########################################


class _Gaussian_Version_Block(char_Block):
    pass


###########################################


class single_float_Block(_Block):
    def __init__(self, arguments, _fh):
        assert arguments[0] == "R"
        self.f = float(arguments[1])

    def get_py(self):
        return self.f


class _Total_Energy_Block(single_float_Block):
    pass


class _IRC_point_Block(float_Block):
    def __init__(self, arguments, fh):
        assert arguments[-3] == "R"
        self.quantity = arguments[1]
        n = int(arguments[-1])
        self.data = read_float_block(fh, n)

    def get_name(self):
        return "_IRC_point_%s" % self.quantity

    def get_py(self):
        return self.data


class _IRC_Number_of_geometries_Block(int_Block):
    pass
