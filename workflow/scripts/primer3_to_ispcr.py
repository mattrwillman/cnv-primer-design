import argparse

def extract_primer_sequences(primer3_output_file):
    """
    Extracts forward, reverse, and internal probe sequences from Primer3 output.
    
    :param primer3_output_file: Path to the Primer3 output file
    :return: List of tuples (forward_primer, reverse_primer, internal_probe)
    """
    primers = []
    forward_primer = None
    reverse_primer = None
    internal_probe = None

    # Read the Primer3 output file
    with open(primer3_output_file, 'r') as file:
        for line in file:
            if line.startswith("PRIMER_LEFT_") and "_SEQUENCE=" in line:
                _, forward_primer = line.strip().split('=')
            elif line.startswith("PRIMER_RIGHT_") and "_SEQUENCE=" in line:
                _, reverse_primer = line.strip().split('=')
            elif line.startswith("PRIMER_INTERNAL_") and "_SEQUENCE=" in line:
                _, internal_probe = line.strip().split('=')

            # When all three sequences are found, add them to the list
            if forward_primer and reverse_primer and internal_probe:
                primers.append((forward_primer, reverse_primer, internal_probe))
                forward_primer = None
                reverse_primer = None
                internal_probe = None

    return primers

def write_to_ispcr_format(primer_sequences, ispcr_output_file, max_product_size=None):
    """
    Writes the extracted primer sequences in IS-PCR format.

    :param primer_sequences: List of tuples (forward_primer, reverse_primer, internal_probe)
    :param ispcr_output_file: Path to the output file for IS-PCR
    :param max_product_size: Maximum product size for IS-PCR (optional)
    """
    with open(ispcr_output_file, 'w') as ispcr_file:
        for forward_primer, reverse_primer, internal_probe in primer_sequences:
            if max_product_size:
                ispcr_file.write(f"{forward_primer} {reverse_primer} {internal_probe} {max_product_size}\n")
            else:
                ispcr_file.write(f"{forward_primer} {reverse_primer} {internal_probe}\n")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert Primer3 output to IS-PCR input format.")
    parser.add_argument("input", help="Primer3 output file")
    parser.add_argument("output", help="IS-PCR input file")
    parser.add_argument("--max_product_size", type=int, help="Maximum product size (optional)", default=None)
    
    args = parser.parse_args()

    # Extract primer sequences from the Primer3 output
    primers = extract_primer_sequences(args.input)

    # Write the IS-PCR input file
    write_to_ispcr_format(primers, args.output, args.max_product_size)

    print(f"IS-PCR input file created: {args.output}")

if __name__ == "__main__":
    main()
