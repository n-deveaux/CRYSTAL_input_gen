from dataclasses import dataclass, field
from ordered_set import OrderedSet
import numpy as np
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# save primitive coordinates and conventional coordinates, handle labels: symbols(all), numbers(primitive only)
# improve code to save lattice
# add instance for atom numbers

@dataclass
class OutputAnalysis:
    """
    A dataclass to analyze the output of a CRYSTAL calculation and 
    extract meaningful data to build property input files.

    Attributes:
        - lines (list): The lines from the CRYSTAL output file.
        - lattice_vectors (list): The lattice vectors of the crystal in Angstrom.
        - lattice_angles (list): The lattice angles in degree.
        - frac_coords (np.array): The fractional coordinates of the atoms in the asymmetric unit.
    """

    lines: list
    lattice_vectors: list = field(default_factory=list)
    lattice_angles: list = field(default_factory=list)
    frac_coords: np.array = field(default_factory=lambda: np.array([]))
    atom_labels: np.array = field(default_factory=lambda: np.array([]))

    def __post_init__(self):
        """
        Parse the lines after initialization.
        """
        self.parse_lines(self.lines)

    def parse_lines(self, lines):
        """
        Parse the lines from the CRYSTAL output file to extract lattice vectors, angles, and fractional coordinates.
        Only the last occurrence is saved (useful when extracting from geometry optimizations).

        :param lines: The lines from the CRYSTAL output file.
        """
        start_lattice = False
        start_coords = False
        frac_coords = []
        atom_labels = []
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

                self.lattice_vectors = [float(i) for i in lattice[:3]]
                self.lattice_angles = [float(i) for i in lattice[3:]]

            # get fractional coordinates and atomic numbers
            elif "ATOMS IN THE ASYMMETRIC UNIT" in line:
                start_coords = True
                frac_coords = []
                atom_labels = []
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
                # if coords[1] == "T":
                frac_coords.append([float(coords[4]), float(coords[5]), float(coords[6])])
                atom_labels.append(coords[3])

        self.frac_coords = np.array(frac_coords)
        self.atom_labels = np.array(atom_labels)

    def get_lattice(self):
        """
        Get the lattice vectors and angles of the crystal and avoid duplicates.

        :return: A tuple containing the lattice vectors and lattice angles in ordered sets.
        """

        lattice_vec = OrderedSet(self.lattice_vectors)
        lattice_ang = OrderedSet(self.lattice_angles)

        return lattice_vec, lattice_ang

    def get_frac_coords(self):
        return self.atom_labels, self.frac_coords
    
    def get_space_group(self) -> int:
        """
        Determine the space group of the crystal using pymatgen.

        :return: the space group number.
        """

        # Create a pymatgen Lattice object
        lattice = Lattice.from_parameters(
            a = self.lattice_vectors[0],
            b = self.lattice_vectors[1],
            c = self.lattice_vectors[2],
            alpha = self.lattice_angles[0],
            beta = self.lattice_angles[1],
            gamma = self.lattice_angles[2],
)
        atomic_species = list(self.atom_labels)

        # Create a pymatgen Structure object
        structure = Structure(
            lattice=lattice,
            species=atomic_species,
            coords=self.frac_coords,
        )

        # Use SpacegroupAnalyzer to determine the space group
        analyzer = SpacegroupAnalyzer(structure)
        space_group_number = analyzer.get_space_group_number()

        return space_group_number

        
