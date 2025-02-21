from pathlib import Path

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
        Handles the case where the basis set is not specified, defined as internal in CRYSTAL or custom.

        :param file: the file object to write to.
        :param basis: the basis set to use.
        """

        def _parse_basisset_file(basis_lines):
            save_basis = False
            basis_block = []
            for line in basis_lines:
                if "## New atom" in line:
                    save_basis = False
                    data = line.split()
                    if data[3] in self.atom_numbers:
                        save_basis = True
                    else:
                        continue
                elif save_basis:
                    basis_block.append(line)

            return basis_block

        if basis.upper() in ['STO-3G', 'STO-6G', 'POB-DZVP', 'POB-DZVPP', 'POB-TZVP', 'POB-DZVP-REV2', 'POB-TZVP-REV2']:
            file.write("BASISSET\n")
            file.write(f"{basis.upper()}\n")
            
        else:
            file.write("END\n")
            basis_file_path = Path(__file__).parent.parent / "basissets" / f"{basis.upper()}.txt"
            try:
                with open(basis_file_path, 'r') as basis_file:
                    basis_lines = basis_file.readlines()
                    basis = _parse_basisset_file(basis_lines)
                
                for i in basis:
                    file.write(i)
                file.write("99 0\n")
                file.write("ENDBS\n")

            except FileNotFoundError:
                print(f"Error: The custom basis set '{basis}' is not available.")

    
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
        file.write(f"{tolinteg1} {tolinteg1} {tolinteg1} {tolinteg2[0]} {tolinteg2[1]}\n")
        file.write("SHRINK\n")
        file.write(f"{shrink} {shrink}\n")
        file.write("MAXCYCLE\n")
        file.write("100\n")
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

        elif input_type.upper() in ['SHG', 'CHI2']:
            file.write("CPKS\n")
            file.write("THIRD\n")

            if wavelength:
                file.write("DYNAMIC\n")
                file.write("1\n")
                file.write(f"{wavelength}\n")

            file.write("MAXCYCLE\n")
            file.write("150\n")
            file.write("END\n")

        elif input_type.upper() == 'OPT':
            file.write("OPTGEOM\n")
            file.write("FULLGEOMOPT\n")
            file.write("END\n")

        else:
            raise KeyError(f"Error: The input type '{input_type}' is not supported.")
        