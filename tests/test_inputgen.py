import unittest
import numpy as np
import os

from inputgen.inputgen import InputGen
from inputgen.outputanalysis import OutputAnalysis

class TestInputGen(unittest.TestCase):
    """
    Unit tests for the CRYSTAL23 input creation in the inputgen module.
    This class tests the each function of the InputGen class.
    """

    def setUp(self):
        """
        Set up the test case by creating a mock OutputAnalysis object.

        Link to an example output file for further tests. 
        """

        self.output_analysis = OutputAnalysis(lines=[])
        self.output_analysis.lattice = [5.12731, 5.12731, 8.70046, 90.00000, 90.00000, 120.00000]
        self.output_analysis.atom_numbers = ['8', '14', '8']
        self.output_analysis.asym_coords = np.array([[-3.333333333333E-01, 3.333333333333E-01, -2.500000000000E-01],
                                                     [-3.333333333333E-01,  3.333333333333E-01, -6.301177619649E-02],
                                                     [0.000000000000,  4.150057771500E-01,  5.043250207322E-21]])
        self.output_analysis.conv_coords = np.array([[-3.333333333333E-01,  3.333333333333E-01, -2.500000000000E-01],
                                                     [ 3.333333333333E-01, -3.333333333333E-01,  2.500000000000E-01],
                                                     [-3.333333333333E-01,  3.333333333333E-01, -6.301177619649E-02],
                                                     [ 3.333333333333E-01, -3.333333333333E-01,  4.369882238035E-01],
                                                     [ 3.333333333333E-01, -3.333333333333E-01,  6.301177619649E-02],
                                                     [-3.333333333333E-01,  3.333333333333E-01, -4.369882238035E-01],
                                                     [ 0.000000000000E+00,  4.144057781498E-01, -4.923236437707E-37],
                                                     [ 0.000000000000E+00, -4.144057781498E-01, -5.000000000000E-01],
                                                     [-4.144057781498E-01, -4.144057781498E-01, -4.923236437707E-37],
                                                     [ 4.144057781498E-01, -6.226556319445E-17, -4.923236437707E-37],
                                                     [-4.144057781498E-01,  6.226556319445E-17, -5.000000000000E-01],
                                                     [ 4.144057781498E-01,  4.144057781498E-01, -5.000000000000E-01]])
        self.output_analysis.atom_labels = ["O", "O", "Si", "Si", "Si", "Si", "O", "O", "O", "O", "O", "O"]

        self.slurm_file_path = 'tests/test_output/slurm-999085.out'

    def test_write_intro(self):
        """
        Test the _write_intro function of the InputGen class.
        1. Create an instance of the InputGen class.
        2. Write the introduction to a file.
        3. Read the content of the file.
        4. Assert that the content contains expected values.
        5. Clean up the file after the test.
        """

        gen_intro = InputGen(self.output_analysis)
        test_intro_file = "tests/test_intro.d12"

        with open(test_intro_file, 'w') as f:
            gen_intro._write_intro(f, input_type="SHG")

        with open(test_intro_file, 'r') as f:
            content = f.read()
            self.assertIn("SHG", content)
            self.assertIn("CRYSTAL", content)
            self.assertIn("0 0 0", content)
        
        os.remove(test_intro_file)

    def test_write_space_group(self):
        """
        Test the _write_space_group function of the InputGen class.
        """

        gen_space_group = InputGen(self.output_analysis)
        test_space_group_file = "tests/test_space_group.d12"

        with open(test_space_group_file, 'w') as f:
            gen_space_group._write_space_group(f)

        with open(test_space_group_file, 'r') as f:
            content = f.read()
            self.assertIn("182", content)

        os.remove(test_space_group_file)

    def test_write_lattice(self):
        """
        Test the _write_lattice function of the InputGen class.
        This test verifies the correct writing of lattice parameters to a file depending 
        on the degeneracy of the lattice and the space group.
        """
        # Test with a degenerate lattice where 90° and 120° angles should be removed.
        gen_lattice = InputGen(self.output_analysis)
        test_degen_lattice_file = "tests/test_degen_lattice.d12"

        with open(test_degen_lattice_file, 'w') as f:
            gen_lattice._write_lattice(f)

        with open(test_degen_lattice_file, 'r') as f:
            content = f.read()
            self.assertEqual(content.count("5.12731"), 1)
            self.assertEqual(content.count("8.70046"), 1)
            self.assertNotIn("90.0", content)
            self.assertNotIn("120.0", content)

        # Test with a non-degenerate lattice where 90° angles should be kept.
        with open(self.slurm_file_path, 'r') as f:
            other_content = f.readlines()

        additional_gen_lattice = OutputAnalysis(lines=other_content)
        test_nondegen_lattice_file = "tests/test_nondegen_lattice.d12"

        gen_nondegen_lattice = InputGen(additional_gen_lattice)

        with open(test_nondegen_lattice_file, 'w') as f:
            gen_nondegen_lattice._write_lattice(f)

        with open(test_nondegen_lattice_file, 'r') as f:
            content = f.read()
            self.assertEqual(content.count("29.478"), 1)
            self.assertEqual(content.count("7.0271"), 1)
            self.assertEqual(content.count("90."), 2)
            self.assertEqual(content.count("99.209"), 1)

        os.remove(test_degen_lattice_file)
        os.remove(test_nondegen_lattice_file)

    def test_write_atomic_coordinates(self):
        """
        Test the _write_atomic_coordinates function of the InputGen class.
        """

        gen_coord = InputGen(self.output_analysis)
        test_coord_file = "tests/test_coord.d12"

        with open(test_coord_file, 'w') as f:
            gen_coord._write_atomic_coordinates(f)

        with open(test_coord_file, 'r') as f:
            content = f.read()
            self.assertEqual(content.count("8"), 2)
            self.assertEqual(content.count("14"), 1)

        os.remove(test_coord_file)

    def test_write_basis_set(self):
        """
        Test the _write_basis_set function of the InputGen class.
        """

        gen_basis = InputGen(self.output_analysis)
        test_basis_file = "tests/internal_basis.d12"
        # custom_basis_file = "tests/custom_basis.d12"

        # Test with an internal basis set
        with open(test_basis_file, 'w') as f:
            gen_basis._write_basis_set(f, basis="POB-DZVP-REV2")

        with open(test_basis_file, 'r') as f:
            content = f.read()
            self.assertIn("POB-DZVP-REV2", content)
            self.assertEqual(content.count("END"), 0)

        # Test with a custom basis set
        # with open(custom_basis_file, 'w') as f:
        #     gen_basis._write_basis_set(f, basis="6-311Gs")

        # with open(custom_basis_file, 'r') as f:
        #     content = f.read()
        #     self.assertIn("END", content)
        #     self.assertIn("99 0", content)
        #     self.assertIn("ENDBS", content)

        os.remove(test_basis_file)
        # os.remove(custom_basis_file)

    def test_write_dft_block(self):
        """
        Test the _write_dft_block function of the InputGen class.
        """

        gen_dft = InputGen(self.output_analysis)
        test_dft_file = "tests/test_dft_block.d12"

        with open(test_dft_file, 'w') as f:
            gen_dft._write_dft_block(f, functional="SVWN", shrink=8, tolinteg1=12, tolinteg2=[20, 60])

        with open(test_dft_file, 'r') as f:
            content = f.read()
            self.assertIn("SVWN", content)
            self.assertIn("SHRINK", content)
            self.assertEqual(content.count("8"), 2)
            self.assertIn("TOLINTEG", content)
            self.assertEqual(content.count("12"), 3)
            self.assertEqual(content.count("20"), 1)
            self.assertEqual(content.count("60"), 1)
            self.assertEqual(content.count("END"), 2)

        os.remove(test_dft_file)

    def test_write_type_info(self):
        """
        Test the _write_type_info function of the InputGen class.
        """

        gen_type = InputGen(self.output_analysis)
        test_type_info_file = "tests/test_type_info.d12"

        with open(test_type_info_file, 'w') as f:
            gen_type._write_type_info(f, input_type="SHG", wavelength=1907)

        with open(test_type_info_file, 'r') as f:
            content = f.read()
            self.assertIn("CPKS", content)
            self.assertIn("THIRD", content)
            self.assertIn("DYNAMIC", content)
            self.assertIn("1907", content)
            self.assertEqual(content.count("END"), 1)

        os.remove(test_type_info_file)
    
    def test_generate_input_file(self):
        """
        Test the generation of input files using the InputGen class.
        This test verifies the global content of the generated input file.
        """
        
        gen = InputGen(self.output_analysis)
        output_file = "tests/cry23.d12"
        
        gen.generate_input(input_type="SHG", wavelength=1907, functional="SVWN", basis="POB-DZVP-REV2", shrink=8, tolinteg1=12, tolinteg2=[20, 60], output_file=output_file)
        
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("182", content)
            self.assertIn("5.12731", content)
            self.assertIn("8.70046", content)
            self.assertNotIn("Si", content)
            self.assertIn("O", content)
            self.assertIn("CPKS", content)
            self.assertIn("DYNAMIC", content)
            self.assertIn("1907", content)
            self.assertIn("POB-DZVP-REV2", content)
            self.assertIn("SVWN", content)
            self.assertIn("SHRINK", content)
            self.assertIn("TOLINTEG", content)

        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
