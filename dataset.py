import os
import re
import csv
import glob

def process_file(input_file, output_file):
    """
    Process a single file and convert its contents to the desired CSV format.
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to the output CSV file
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content into lines and filter out empty lines
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Prepare the output data
    output_data = []
    id_counter = 1
    
    # Iterate through the lines to pair them
    i = 0
    while i < len(lines):
        # Extract the first speaker's message
        line1 = lines[i]
        matches1 = re.match(r'([GV])\|(.*?)\|', line1)
        if not matches1:
            i += 1
            continue
            
        speaker1 = matches1.group(1)
        message1 = matches1.group(2).strip()
        
        # Check if we have a next line for the second speaker
        if i + 1 < len(lines):
            line2 = lines[i + 1]
            matches2 = re.match(r'([GV])\|(.*?)\|', line2)
            if matches2:
                speaker2 = matches2.group(1)
                message2 = matches2.group(2).strip()
                
                # Create the paired entry
                paired_message = f"{speaker1}: {message1} | {speaker2}: {message2}"
                output_data.append([id_counter, paired_message])
                id_counter += 1
                i += 2  # Move to the next pair
            else:
                # If the next line doesn't match, just use the current line
                output_data.append([id_counter, f"{speaker1}: {message1}"])
                id_counter += 1
                i += 1
        else:
            # If there's no next line, just use the current line
            output_data.append([id_counter, f"{speaker1}: {message1}"])
            id_counter += 1
            i += 1
    
    # Write to the CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'sentence'])
        writer.writerows(output_data)

def process_directory(input_pattern, output_dir):
    """
    Process multiple files matching the input pattern and convert them to CSV files.
    
    Args:
        input_pattern (str): Glob pattern for input files
        output_dir (str): Directory to save output CSV files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all matching files
    for input_file in glob.glob(input_pattern):
        base_name = os.path.basename(input_file)
        file_name, _ = os.path.splitext(base_name)
        output_file = os.path.join(output_dir, f"{file_name}.csv")
        
        print(f"Processing {input_file} -> {output_file}")
        process_file(input_file, output_file)
        print(f"Done processing {input_file}")

import csv

def add_columns_to_csv(input_file, output_file, column1_name, column1_value, column2_name, column2_value):
    # Open the input file
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        # Get the header and data rows
        header = next(reader)
        rows = list(reader)
    
    # Add new column names to header
    header.append(column1_name)
    header.append(column2_name)
    
    # Add new column values to each row
    for row in rows:
        row.append(column1_value)
        row.append(column2_value)
    
    # Write to output file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(rows)
    
    print(f"Successfully added columns '{column1_name}' and '{column2_name}' to CSV file.")

'''# Example usage
if __name__ == "__main__":
    input_file = "sample_5.csv/samples_5.csv"  # Replace with your input file name
    output_file = "data_sintetici_csv/ds_5.csv"  # Replace with your output file name
    column1_name = "tag"  # Replace with your first column name
    column1_value = "reframing"  # Replace with your first column value
    column2_name = "phase"  # Replace with your second column name
    column2_value = "isolation"  # Replace with your second column value
    
    add_columns_to_csv(input_file, output_file, column1_name, column1_value, column2_name, column2_value)'''


import pandas as pd
import os
import glob

def concatenate_csv_files(input_folder, output_file, file_pattern="*.csv"):
    """
    Concatenate multiple CSV files with the same column structure.
    
    Parameters:
    - input_folder: Folder containing CSV files to concatenate
    - output_file: Path for the output concatenated CSV file
    - file_pattern: Pattern to match CSV files (default is all .csv files)
    """
    # Get list of all CSV files in the input folder matching the pattern
    csv_files = glob.glob(os.path.join(input_folder, file_pattern))
    
    if not csv_files:
        print(f"No CSV files found in {input_folder} matching pattern '{file_pattern}'")
        return
    
    # Create an empty list to store dataframes
    dfs = []
    
    # Read each CSV file and append to the list
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"Added {file} - {len(df)} rows")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if not dfs:
        print("No valid CSV files were found to concatenate.")
        return
    
    # Concatenate all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Save to output file
    combined_df.to_csv(output_file, index=False)
    print(f"Successfully concatenated {len(dfs)} CSV files to {output_file}")
    print(f"Total rows: {len(combined_df)}")

# Example usage
if __name__ == "__main__":
    input_folder = "data_sintetici_csv"  # Replace with your folder containing CSV files
    output_file = "dataset_sintetico.csv"  # Replace with your desired output filename
    
    concatenate_csv_files(input_folder, output_file)

'''# Example usage
if __name__ == "__main__":
    # To process a single file
    # process_file("input.txt", "output.csv")
    
    # To process multiple files
    process_directory("dataset/samples_5.txt", "sample_5.csv")'''