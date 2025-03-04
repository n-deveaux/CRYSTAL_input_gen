import unittest

from inputgen.outputanalysis import OutputAnalysis

class TestOutputAnalysis(unittest.TestCase):
    """
    Unit tests for the CRYSTAL23 ouput analysis in the inputgen module.
    This class tests the each function of the OutputAnalysis class.

    To obtain an output example, a geometry optimmization calculation was performed
    on a test system using the CRYSTAL23 code.
    """

    def setUp(self):
        """
        Set up the test case by reading the output file and creating an OutputAnalysis object.
        """

        file_path = 'tests/test_output/slurm-983371.out'
        
        with open(file_path, 'r') as f:
            self.lines = f.readlines()
        
        self.output_analysis = OutputAnalysis(lines=self.lines)

    def test_parse_lines(self):
        """
        Test the parse_lines function of the OutputAnalysis class.
        Assert that the attributes lengths are as expected.
        """

        self.assertEqual(len(self.output_analysis.lattice), 6)
        self.assertEqual(len(self.output_analysis.conv_coords), 66)
        self.assertEqual(len(self.output_analysis.asym_coords), 33)
        self.assertEqual(len(self.output_analysis.atom_labels), 66)
        self.assertEqual(len(self.output_analysis.atom_numbers), 33)

    def test_get_lattice(self):
        """
        Test the get_lattice function of the OutputAnalysis class.
        """

        lattice = self.output_analysis.get_lattice()
        self.assertEqual(len(lattice), 5)

    def test_get_frac_coords(self):
        """
        Test the get_frac_coords function of the OutputAnalysis class.
        """

        atom_numbers, asym_coords = self.output_analysis.get_frac_coords()
        self.assertEqual(len(atom_numbers), 33)
        self.assertEqual(len(asym_coords), 33) 

    def test_get_space_group(self):
        """
        Test the get_space_group function of the OutputAnalysis class.
        """
       
        space_group = self.output_analysis.get_space_group()
        self.assertEqual(space_group, 7)

if __name__ == '__main__':
    unittest.main()