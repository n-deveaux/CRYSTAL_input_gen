class InputGen:
    def __init__(self, output_analysis):
        """
        Initialize the InputGen class with an instance of OutputAnalysis.
        """

        self.lattice_vectors, self.lattice_angles = output_analysis.get_lattice()
        self.atom_numbers, self.frac_coords = output_analysis.get_frac_coords()
        self.space_group = output_analysis.get_space_group()

    def generate_input(self, input_type, wavelength):
        """
        Generate a new CRYSTAL input file based on the extracted data.
        """

        print("Lattice Vectors:", self.lattice_vectors)
        print("Lattice Angles:", self.lattice_angles)
        print("coords:", self.frac_coords)
        print("coords:", self.atom_numbers)
        print("Space Group:", self.space_group)

# do not forget to transform lattice in set and add condition to not print 90 and 120° angles