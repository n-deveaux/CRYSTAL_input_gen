from pathlib import Path

# create _write_intro method
# create exception if input_type is not 'chi2' or 'opt'
# handle basis set


class InputGen:
    """
    A class to generate a new CRYSTAL input file based on the extracted data
    from an OutputAnalysis instance. 

    Different input types can be generated based on the user's needs:
        - chi2: second-order nonlinear susceptibility, can be generated for different wavelengths.
        - opt: geometry optimization (from the last extracted geometry).

    Attributes:
        - lattice (orderedset): The nonredundant lattice vectors and angles.
        - atom_numbers (list): The atomic numbers of the atoms in the asymetric unit.
        - frac_coords (np.array): The fractional coordinates of the atoms in the asymetric unit.
        - space_group (int): The space group of the crystal.
    """

    def __init__(self, output_analysis):
        """
        Initialize the InputGen class with an instance of OutputAnalysis.
        """

        self.lattice = output_analysis.get_lattice()
        self.atom_numbers, self.frac_coords = output_analysis.get_frac_coords()
        self.space_group = output_analysis.get_space_group()

    def generate_input(self,
                       input_type,
                       wavelength,
                       functional,
                       basis,
                       shrink,
                       tolinteg1,
                       tolinteg2,
                       output_file="cry23.d12"):
        """
        Generate a new CRYSTAL input file and write it to the specified output file.

        :param input_type: type of input file to generate (e.g., 'sp', 'opt', 'chi2').
        :param wavelength: wavelength of the light source (for 'chi2' calculations).
        :param output_file: path and name to the output file (default: 'cry.d12').
        """

        output_path = Path(output_file)

        with output_path.open("w") as f:
            self._write_intro(f, input_type)
            self._write_space_group(f)
            self._write_lattice(f)
            self._write_atomic_coordinates(f)
            self._write_type_info(f, input_type, wavelength)
            self._write_basis_set(f, basis)
            self._write_dft_block(f, functional, shrink, tolinteg1, tolinteg2)

    def _write_intro(self, file, input_type):
        """
        Write the introduction to the file.

        :param file: the file object to write to.
        :param input_type: type of input file to generate.
        """

        if input_type:
            file.write(input_type.upper())
        else:
            file.write("TITLE")

        file.write("\nCRYSTAL\n")
        file.write("0 0 0\n")

    def _write_space_group(self, file):
        """
        Write space group number to the file.

        :param file: the file object to write to.
        """

        file.write(f"{self.space_group}\n")

    def _write_lattice(self, file):
        """
        Write lattice parameters to the file.

        :param file: the file object to write to.
        """

        for param in self.lattice:
            if float(param) in [90., 120.]:
                continue
            file.write(f"{param} ")
        file.write("\n")

    def _write_atomic_coordinates(self, file):
        """
        Write atomic coordinates to the file.

        :param file: the file object to write to.
        """

        file.write(f"{len(self.atom_numbers)}\n")
        for atom_num, coords in zip(self.atom_numbers, self.frac_coords):
            file.write(f"{atom_num}     {coords[0]}     {coords[1]}     {coords[2]}\n")

    def _write_basis_set(self, file, basis):
        """
        Write the basis set to the file.

        :param file: the file object to write to.
        :param basis: the basis set to use.
        """

        file.write(f"{basis}\n")
        file.write("ENDBS\n")
    
    def _write_dft_block(self, file, functional, shrink, tolinteg1, tolinteg2):
        """
        Write the DFT block to the file.

        :param file: the file object to write to.
        :param functional: the DFT exchange-correlation functional to use.
        :param shrink: the SHRINK parameters for the sampling of the first BZ.
        :param tolinteg1: the three first entries of the TOLINTEG parameter.
        :param tolinteg2: the two last entries of the TOLINTEG parameter.
        """

        file.write("DFT\n")
        file.write(f"{functional}\n")
        file.write("END\n")
        file.write("TOLINTEG\n")
        file.write(f"{tolinteg1} {tolinteg2}\n")
        file.write("SHRINK\n")
        file.write(f"{shrink}\n")
        file.write("MAXCYCLE\n")
        file.write("150\n")
        file.write("END\n")

    def _write_type_info(self, file, input_type, wavelength):
        """
        Write input type-specific information to the file.

        :param file: the file object to write to.
        :param input_type: type of input file to generate.
        :param wavelength: wavelength of the light source.
        """

        if input_type is None:
            pass

        if input_type == 'chi2':
            file.write("CPKS\n")
            file.write("THIRD\n")

            if wavelength:
                file.write("DYNAMIC\n")
                file.write("1\n")
                file.write(f"{wavelength}\n")

            file.write("MAXCYCLE\n")
            file.write("150\n")
            file.write("END\n")

        elif input_type == 'opt':
            file.write("OPTGEOM\n")
            file.write("FULLGEOMOPT\n")
            file.write("END\n")

        file.write("END\n")