import os
import csv
import argparse
import time

def create_csv_from_path(abs_path, csv_filename):
    # Ensure the provided path is absolute
    if not os.path.isabs(abs_path):
        raise ValueError("The provided path must be an absolute path.")
    
    # Split the path into its components
    path_components = abs_path.split(os.sep)
    
    # Create the CSV file and write the header
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['file path', 'start timestamp', 'end timestamp', 'smite scored?'])
        
        # Generate the full path for each folder in the path and write to the CSV
        for i in os.listdir(abs_path):
            if((".MP4" in i) or (".mp4" in i)):
                csv_writer.writerow([abs_path+i, '', '', ''])

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a CSV file with a row for every folder in the given absolute file path.')
    parser.add_argument('abs_path', type=str, help='The absolute file path.')
    parser.add_argument('csv_filename', type=str, help='The output CSV file name.')

    # Parse arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    create_csv_from_path(args.abs_path, args.csv_filename)

if __name__ == "__main__":
    main()
