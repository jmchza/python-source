import csv
import re
import argparse
import os
import sys

def strip_pattern_from_csv(input_file, output_file, pattern):
    csv.field_size_limit(sys.maxsize)
    
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            # Apply regex to each cell in the row
            new_row = [re.sub(pattern, '', cell) for cell in row]
            writer.writerow(new_row)


# Initialize parser
parser = argparse.ArgumentParser(description="Initializing the parser")

parser.add_argument("-n", "--file", type=str, help="Name of the file to remove REG and VIN from Comments")
parser.add_argument("-f", "--folder", type=str, help="Name of the remote Folder in the sftp server to place the fle into")
parser.add_argument("-c", "--cleanup", type=str, help="Set to true if you want to delete all intermedium files at the end")

args = parser.parse_args()
intermedium_file = 'int.csv'

if args.file:
    print(f"Processing file: {args.file} ..... {os.sep}")
if args.folder:
    strip_pattern_from_csv(args.file, os.path.join(args.folder, intermedium_file), r'REG#\[.+\]')
    
    file_name_list = args.file.split(".")
    
    if "/" in file_name_list[0]:
        file_name_array = file_name_list[0].split("/")
        file_name = file_name_array[-1]
    else:
        file_name = file_name_list[0]
    print(file_name)

    output_file = os.path.join(args.folder, file_name + '.cleanedup.' + file_name_list[-1])

    print(f"Stripping second pattern from intermedium files: {os.path.join(args.folder, intermedium_file)}")
    strip_pattern_from_csv(os.path.join(args.folder, intermedium_file), output_file, r'VIM#\[.+\]')
    
else:
    print("ERROR: Remote sftp folder has not been configured")
if args.cleanup:
    print(f"Cleaning up intermedium files... {intermedium_file}")
    os.remove(f"{os.path.join(args.folder, intermedium_file)}")
