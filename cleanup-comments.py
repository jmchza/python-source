import csv
import re
import argparse
import os
import sys
import pyodbc

def strip_pattern_from_csv(input_file, output_file, pattern, replacedWith=''):
    csv.field_size_limit(sys.maxsize)
    
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            # Apply regex to each cell in the row
            new_row = [re.sub(pattern, replacedWith, cell) for cell in row]
            writer.writerow(new_row)


def connect_and_dump_to(query, output_file, pattern, replacedWith=''):

    # Define your connection parameters
    server = os.getenv("SERVER_NAME",'your_server_name')
    database = os.getenv("SERVER_DB",'your_server_db')
    username = os.getenv("SERVER_USER",'your_server_username')
    password = os.getenv("SERVER_PW",'your_server_password')

    # Create the connection string
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Establish the connection
    connection = pyodbc.connect(connection_string)

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a query
    cursor.execute(query)
    with open(output_file, 'w', newline='') as outfile:
        # Fetch and print the result
        row = cursor.fetchone()
        print(f"row:  {type(row)} len: {len(row)}")
        writer = csv.writer(outfile)
        
        new_row = [re.sub(pattern, replacedWith, cell) for cell in row[0]]
        writer.writerow(new_row)
        
    # Close the connection
    connection.close()



# Initialize parser
parser = argparse.ArgumentParser(description="Initializing the parser")

parser.add_argument("-n", "--file", type=str, help="Name of the file to remove REG and VIN from Comments")
parser.add_argument("-f", "--folder", type=str, help="Name of the remote Folder in the sftp server to place the fle into")
parser.add_argument("-c", "--cleanup", type=str, help="Set to true if you want to delete all intermedium files at the end")
parser.add_argument("-d", "--useDB", type=str, help="Set to true if you want to extract data from DB first instead of providing a source file")

args = parser.parse_args()
intermedium_file = 'int.csv'

if args.useDB and args.file and args.folder:
    connect_and_dump_to("SELECT comments FROM tbl_CRM_LeadConversion", args.file, r'REG#\[.+\]')
if args.file:
    print(f"Processing file: {args.file} .....")
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
