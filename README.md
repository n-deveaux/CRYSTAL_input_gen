# `CRYSTAL_input_gen`

This project generates input files for the `CRYSTAL23` software (see the [website](https://www.crystal.unito.it)) from output files. It extracts necessary parameters from the output files of previous calculations and creates new input files suitable for various types of calculations, such as geometry optimization and second-order nonlinear susceptibility.

## Overview

- Analyzes CRYSTAL output files to extract lattice vectors, atomic coordinates, and space group.
- Generates CRYSTAL input files for different types of calculations (single point, linear electric susceptibility $\chi^{(1)}$ and second-order nonlinear electric susceptibility $\chi^{(2)}$ (from second harmonic generation), and geometry optimizations).
- Supports specifying parameters such as wavelength, DFT functional, basis set, SHRINK and TOLINTEG parameters.

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install git+https://github.com/n-deveaux/CRYSTAL_input_gen.git
```

This will install the following dependencies:
- `numpy`
- `ordered-set`
- `pymatgen`

## Usage

Run the `crystal-input-gen` script to read a CRYSTAL output file and generate a new input file:

```bash
crystal-input-gen <inputfile> -t <type> -w <wavelength> -xcf <functional> -b <basis> -s <shrink> -t1 <tolinteg1> -t2 <tolinteg2>
```

### Command Line Arguments

- `inputfile`: A CRYSTAL output file to read.
- `-t`, `--type`: The type of input file to generate [SP (no argument), chi2 (or SHG), opt].
- `-w`, `--wavelength`: The wavelength of the light source (nm).
- `-xcf`, `--functional`: The DFT exchange-correlation functional to use (default: wB97X).
- `-b`, `--basis`: The basis set to use (default: 6-31Gs).
- `-s`, `--shrink`: The SHRINK parameters for the sampling of the irreducible first Brillouin zone (default: 4).
- `-t1`, `--tolinteg1`: The three first entries of the TOLINTEG parameter (default: 7).
- `-t2`, `--tolinteg2`: The two last entries of the TOLINTEG parameter (default: 18 40).

## Available Basis Sets

The following basis sets are supported for all the atoms of the periodic table, since they are used as `CRYSTAL23` internal basis sets (see [user manual](https://www.crystal.unito.it/include/manuals/crystal23.pdf) for more details).

```python
custom_basis_sets = ["STO-3G", "STO-6G", "POB-DZVP", "POB-DZVPP", "POB-TZVP", "POB-DZVP-REV2", "POB-TZVP-REV2"]
```

Additionally, custom basis sets can be specified by providing the name of a basis set available in the `basissets` directory. In the latter, the following basis sets are available

```python
internal_basis_sets = ["6-31G", "6-31G2(2df,p)", "6-31G*", "6-31G**", "6-311G", "6-311G*", "6-311G**", "cc-PVDZ", "cc-PVTZ", "cc-PVQZ", "def2-SVP", "def2-SVPD", "def2-TZVP", "Ahlrichs VDZ", "pVDZ", "VTZ"]
```

for the following atoms
```python
atoms = ["H", "B", "C", "N", "O", "F", "Al", "Si", "P", "S", "Cl"]
```
These custom basis sets originate from the [Basis Set Exchange](https://www.basissetexchange.org) platform, and the orbital occupancies were filled
according to a *Klechkowski* (or *Madelung*) -like fashion.

**Note:** The current version of the code only allows defining one basis set for all atoms.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository, then clone the fork (see [there](https://guides.github.com/activities/forking/)).
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "**Created** new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a merge request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future development
- Add feature to generate input from `xyz` files and unit cell parameters.
- Add support for different basis sets for each atom in a single input file.