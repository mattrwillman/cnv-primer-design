import csv
import argparse

def parse_primer3_output(input_file, output_file):
    """
    Parse Primer3 output and convert it into a table with one row per SEQUENCE_ID-by-primer pair combination,
    including primer TM values, product TM values, and primer pair index, while removing the index from all 
    column names except the PRIMER_PAIR_INDEX. The columns will be ordered as requested.
    
    Args:
        input_file (str): Path to the Primer3 output file.
        output_file (str): Path to the output CSV file.
    """
    try:
        # Open the Primer3 output file
        with open(input_file, 'r') as file:
            lines = file.readlines()
        
        records = []
        current_record = {}
        sequence_id = None

        for line in lines:
            line = line.strip()
            if line.startswith("="):  # End of a record
                if current_record:  # Save the current record
                    sequence_id = current_record.get("SEQUENCE_ID", "Unknown")
                    primer_pairs = extract_primer_pairs(current_record)
                    for pair in primer_pairs:
                        records.append({"SEQUENCE_ID": sequence_id, **pair})
                current_record = {}
            elif "=" in line:  # Key-value pair
                key, value = line.split("=", 1)
                current_record[key.strip()] = value.strip()

        # Add the last record if not empty
        if current_record:
            sequence_id = current_record.get("SEQUENCE_ID", "Unknown")
            primer_pairs = extract_primer_pairs(current_record)
            for pair in primer_pairs:
                records.append({"SEQUENCE_ID": sequence_id, **pair})

        # Define the desired column order
        column_order = [
            "SEQUENCE_ID",
            "PRIMER_PAIR_INDEX",
            "PRIMER_LEFT_SEQUENCE",
            "PRIMER_RIGHT_SEQUENCE",
            "PRIMER_LEFT_TM",
            "PRIMER_RIGHT_TM",
            "PRIMER_PAIR_PRODUCT_SIZE",
            "PRIMER_PAIR_PRODUCT_TM"
        ]

        # Write to a CSV file with the defined column order
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_order)
            writer.writeheader()  # Write the header row
            writer.writerows(records)  # Write all records as rows

        print(f"Primer3 output has been converted to a table and saved in '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_primer_pairs(record):
    """
    Extract primer pair information from a Primer3 record, including Tm values, product Tm values, and primer pair index.
    
    Args:
        record (dict): Dictionary of key-value pairs for a single SEQUENCE_ID.
    
    Returns:
        list: A list of dictionaries with primer pair details.
    """
    pairs = []
    pair_indices = set()
    
    # Find all primer pair indices
    for key in record.keys():
        if key.startswith("PRIMER_LEFT_") and key[len("PRIMER_LEFT_")].isdigit():
            index = key.split("_")[2]
            pair_indices.add(index)

    # Create a dictionary for each pair, including Tm, Product Tm values, and Primer Pair Index
    for index in sorted(pair_indices):
        pair = {
            f"PRIMER_LEFT_SEQUENCE": record.get(f"PRIMER_LEFT_{index}_SEQUENCE", ""),
            f"PRIMER_RIGHT_SEQUENCE": record.get(f"PRIMER_RIGHT_{index}_SEQUENCE", ""),
            f"PRIMER_PAIR_PRODUCT_SIZE": record.get(f"PRIMER_PAIR_{index}_PRODUCT_SIZE", ""),
            f"PRIMER_LEFT_TM": record.get(f"PRIMER_LEFT_{index}_TM", ""),
            f"PRIMER_RIGHT_TM": record.get(f"PRIMER_RIGHT_{index}_TM", ""),
            f"PRIMER_PAIR_PRODUCT_TM": record.get(f"PRIMER_PAIR_{index}_PRODUCT_TM", ""),
            f"PRIMER_PAIR_INDEX": index  # Add the index value here
        }
        pairs.append(pair)

    return pairs

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert Primer3 output to a table with one row per SEQUENCE_ID-by-primer pair, including primer TM values, product TM values, and primer pair index.")
    parser.add_argument("input_file", help="Path to the Primer3 output file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    args = parser.parse_args()

    # Call the function with provided arguments
    parse_primer3_output(args.input_file, args.output_file)
