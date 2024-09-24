import argparse

def parse_primer3_output(primer3_file):
    """Parses the Primer3 output file to extract multiple forward and reverse primer sequences."""
    primers = {}
    seq_id = None

    with open(primer3_file, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Parse SEQUENCE_ID
            if line.startswith("SEQUENCE_ID="):
                seq_id = line.split("=")[1]
                if seq_id not in primers:
                    primers[seq_id] = []
            
            # Only process lines that contain primer sequences (those containing _SEQUENCE=)
            if "PRIMER_LEFT_" in line and "_SEQUENCE=" in line:
                # Extract the primer index from the key
                primer_index = line.split('_')[2].split('_')[0]
                forward_primer = line.split("=")[1]
                
                # Ensure the list has room for this primer index
                while len(primers[seq_id]) <= int(primer_index):
                    primers[seq_id].append({'forward': '', 'reverse': ''})
                
                primers[seq_id][int(primer_index)]['forward'] = forward_primer
            
            if "PRIMER_RIGHT_" in line and "_SEQUENCE=" in line:
                primer_index = line.split('_')[2].split('_')[0]
                reverse_primer = line.split("=")[1]
                
                # Ensure the list has room for this primer index
                while len(primers[seq_id]) <= int(primer_index):
                    primers[seq_id].append({'forward': '', 'reverse': ''})
                
                primers[seq_id][int(primer_index)]['reverse'] = reverse_primer

    return primers

def write_ispcr_input(primers, ispcr_file):
    """Writes the ISPCR input format from the parsed Primer3 primers."""
    with open(ispcr_file, 'w') as file:
        for seq_id, primer_pairs in primers.items():
            for idx, primer_data in enumerate(primer_pairs):
                file.write(f"{seq_id}_pair{idx+1} {primer_data['forward']} {primer_data['reverse']}\n")

def main():
    parser = argparse.ArgumentParser(description="Convert Primer3 output to ISPCR input format with multiple primer pairs")
    parser.add_argument('primer3_output', help="The Primer3 output file")
    parser.add_argument('ispcr_input', help="The output file for ISPCR")

    args = parser.parse_args()

    # Parse Primer3 output file
    primers = parse_primer3_output(args.primer3_output)

    # Write to ISPCR input format
    write_ispcr_input(primers, args.ispcr_input)

if __name__ == "__main__":
    main()
