class InputGen:
    def __init__(self, output_analysis):
        """
        Initialize the InputGen class with an instance of OutputAnalysis.
        """

        self.lattice = output_analysis.get_lattice()
        self.atom_numbers, self.frac_coords = output_analysis.get_frac_coords()
        self.space_group = output_analysis.get_space_group()

    def generate_input(self, input_type, wavelength):
        """
        Generate a new CRYSTAL input file based on the extracted data.
        """

        print("Lattice:", self.lattice)
        print("coords:", self.frac_coords)
        print("atoms:", self.atom_numbers)
        print("Space Group:", self.space_group)

# do not forget to add condition to not print 90 and 120° angles