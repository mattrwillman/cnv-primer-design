#!/usr/bin/env python

import sys
from Bio import AlignIO

def generate_consensus(input_file, output_file):
    """
    Parse a ClustalW alignment file and generate a single-sequence FASTA file.
    Non-conserved nucleotides are replaced with 'N'.
    """
    # Load the ClustalW alignment
    alignment = AlignIO.read(input_file, "clustal")

    # Initialize the consensus sequence
    consensus_sequence = []

    # Iterate through each column in the alignment
    alignment_length = alignment.get_alignment_length()
    for i in range(alignment_length):
        column = alignment[:, i]  # Extract the column (nucleotides at this position)
        unique_bases = set(column)
        
        if len(unique_bases) == 1:  # If all bases are the same (conserved)
            consensus_sequence.append(unique_bases.pop())  # Add the conserved base
        else:
            consensus_sequence.append("N")  # Non-conserved positions are replaced with 'N'

    # Create the FASTA output
    with open(output_file, "w") as output:
        output.write(">consensus_sequence\n")
        output.write("".join(consensus_sequence) + "\n")

    print(f"Consensus sequence written to {output_file}")

if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file.aln> <output_file.fasta>")
        sys.exit(1)
    
    # Get file paths from command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the consensus generation function
    generate_consensus(input_file, output_file)
