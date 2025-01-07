import argparse

from .outputanalysis import OutputAnalysis
from .inputgen import InputGen

def main():
    """
    Read the CRYSTAL output file and allow command line input.
    """

    parser = argparse.ArgumentParser(description='Read a CRYSTAL output file and generate a new input file.')
    parser.add_argument('inputfile', help='A CRYSTAL output file to read')
    parser.add_argument('-t', '--type', help='The type of input file to generate', default=None)
    parser.add_argument('-w', '--wavelength', help='The wavelength of the light source (nm)', default=None)
    parser.add_argument('-xcf', '--functional', help='The DFT exchange-correlation functional to use', default='wB97X')
    parser.add_argument('-b', '--basis', help='The basis set to use', default='6-31Gd')
    parser.add_argument('-s', '--shrink', help='The SHRINK parameters for the sampling of the first BZ', default='4 4')
    parser.add_argument('-t1', '--tolinteg1', help='The three first entries of the TOLINTEG parameter', default='7 7 7')
    parser.add_argument('-t2', '--tolinteg2', help='The two last entries of the TOLINTEG parameter', default='18 40')
    args = parser.parse_args()

    try:
        with open(args.inputfile, 'r') as file:
            lines = file.readlines()
        
    except FileNotFoundError:
        print(f"Error: The file '{args.inputfile}' was not found.")
    
    # Analyze the output
    output_analysis = OutputAnalysis(lines)

    # Generate the input file
    gen = InputGen(output_analysis)
    gen.generate_input(args.type,
                       args.wavelength,
                       args.functional,
                       args.basis,
                       args.shrink,
                       args.tolinteg1,
                       args.tolinteg2
                       )

if __name__ == '__main__':
    main()

