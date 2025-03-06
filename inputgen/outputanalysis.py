from dataclasses import dataclass, field
import numpy as np
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

@dataclass
class OutputAnalysis:
    """
    A dataclass to analyze the output of a CRYSTAL calculation and 
    extract meaningful data to build property input files.

    Attributes:
        - lines (list): The lines from the CRYSTAL output file.
        - lattice_vectors (list): The lattice vectors of the crystal in Angstrom.
        - lattice_angles (list): The lattice angles in degree.
        - conv_coords (list): The fractional coordinates of the atoms in the conventional unit.
        - asym_coords (np.array): The fractional coordinates of the atoms in the asymetric unit.
        - atom_labels (list): The labels of the atoms in the conventional unit.
        - atom_numbers (list): The atomic numbers of the atoms in the asymetric unit.
    """

    lines: list
    lattice: list = field(default_factory=list)
    conv_coords: list = field(default_factory=list)
    asym_coords: np.array = field(default_factory=lambda: np.array([]))
    atom_labels: list = field(default_factory=list)
    atom_numbers: list = field(default_factory=list)

    def __post_init__(self):
        """
        Parse the lines after initialization.
        """

        self._parse_lines(self.lines)

    def _parse_lines(self, lines):
        """
        Parse the lines from the CRYSTAL output file to extract lattice vectors, angles, and fractional coordinates.
        Only the last occurrence is saved (useful when extracting from geometry optimizations).

        :param lines: The lines from the CRYSTAL output file.
        """

        start_lattice = False
        start_coords = False
        asym_coords = []
        for line in lines:
            # get lattice vectors and angles
            if "LATTICE PARAMETERS" in line:
                start_lattice = True
            elif "**" in line:
                start_lattice = False
            elif start_lattice:
                lattice = line.split()
                if len(lattice) != 6:
                    continue
                # Check if the first element is numeric
                try:
                    float(lattice[0])
                except ValueError:
                    continue

                self.lattice = [float(i) for i in lattice]

            # get fractional coordinates and atomic numbers
            elif "ATOMS IN THE ASYMMETRIC UNIT" in line:
                start_coords = True
                self.conv_coords = []
                asym_coords = []
                self.atom_labels = []
                self.atom_numbers = []
            elif "T = ATOM BELONGING TO THE ASYMMETRIC UNIT" in line:
                start_coords = False
            elif start_coords:
                coords = line.split()
                if len(coords) != 7:
                    continue
                try:
                    float(coords[4])
                except ValueError:
                    continue

                # Save the conventional coordinates and labels for space group determination
                self.conv_coords.append([float(coords[4]), float(coords[5]), float(coords[6])])
                self.atom_labels.append(coords[3])

                # Save the asymetric coordinates and atomic numbers
                if coords[1] == "T":
                    asym_coords.append([coords[4], coords[5], coords[6]])
                    self.atom_numbers.append(coords[2])

        self.asym_coords = np.array(asym_coords)

    def get_lattice(self) -> np.array:
        """
        Get the lattice vectors and angles of the crystal and avoid duplicates.

        :return: A numpy array containing the lattice vectors and lattice angles.
        """

        lattice_param = np.array(self.lattice)

        return lattice_param

    def get_frac_coords(self) -> tuple:
        """
        Get the fractional coordinates of the atoms in the asymetric unit and their atomic numbers.

        :return: A tuple of strings containing the atomic numbers and fractional coordinates.
        """

        return self.atom_numbers, self.asym_coords
    
    def get_space_group(self) -> int:
        """
        Determine the space group of the crystal using pymatgen.

        :return: the space group number.
        """

        # Create a pymatgen Lattice object
        lattice = Lattice.from_parameters(
            a = self.lattice[0],
            b = self.lattice[1],
            c = self.lattice[2],
            alpha = self.lattice[3],
            beta = self.lattice[4],
            gamma = self.lattice[5]
        )

        # Create a pymatgen Structure object
        structure = Structure(
            lattice=lattice,
            species=self.atom_labels,
            coords=self.conv_coords
        )

        # Use SpacegroupAnalyzer to determine the space group
        analyzer = SpacegroupAnalyzer(structure)
        space_group_number = analyzer.get_space_group_number()

        return space_group_number

        
