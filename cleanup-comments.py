import csv
import re
import argparse
import os
import sys
import pyodbc
import psycopg2



def strip_pattern_from_csv(srcFileOrIntNumber, input_file, folder, pattern, isIntermedium=False, replacedWith=''):
    csv.field_size_limit(sys.maxsize)
    # print(f"{srcFileOrIntNumber}, {input_file}, {folder}")
    if isIntermedium:
        intermedium_file = f"int.{srcFileOrIntNumber}.csv"
        output_file = os.path.join(folder, intermedium_file)
    else:
        file_name_list = srcFileOrIntNumber.split(".")
        file_name = get_file_name(file_name_list)
        
        output_file = os.path.join(folder, file_name + '.cleanedup.' + file_name_list[-1])
        
    print(f"Input File: {input_file}, Output File: {output_file}")

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            # Apply regex to each cell in the row
            new_row = [re.sub(pattern, replacedWith, cell) for cell in row]
            writer.writerow(new_row)
    return output_file
            
def get_file_name(file_name_list):
    
    if "/" in file_name_list[0]:
        file_name_array = file_name_list[0].split("/")
        return file_name_array[-1]
    
    return file_name_list[0]


def connect_and_dump_to(query, output_file, pattern, replacedWith=''):

    # Define your connection parameters
    server = os.getenv("SERVER_NAME",'your_server_name')
    database = os.getenv("SERVER_DB",'your_server_db')
    username = os.getenv("SERVER_USER",'your_server_username')
    password = os.getenv("SERVER_PW",'your_server_password')
    
    # Connect to postgres
    # connection = psycopg2.connect(
    #     dbname=database,
    #     user=username,
    #     password=password,
    #     host=server
    # )

    # # Create the connection string
    connection_string = f'DRIVER={'ODBC Driver 18 for SQL Server'};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Connect to SQL Server
    connection = pyodbc.connect(connection_string)

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a query
    cursor.execute(query)
    
    row = cursor.fetchone()
    with open(output_file, 'w', newline='') as outfile:
        # Fetch and print the result
        while row is not None:
            print(f"row:  {type(row)} len: {len(row)}")
            writer = csv.writer(outfile)
            print(row)
            new_row = [re.sub(pattern, replacedWith, str(cell)) for cell in row]
            writer.writerow(new_row)
            row = cursor.fetchone()
                
        
    # Close the connection
    connection.close()

# Initialize parser
parser = argparse.ArgumentParser(description="Initializing the parser")

parser.add_argument("-n", "--file", type=str, help="Name of the file to remove REG and VIN from Comments")
parser.add_argument("-f", "--folder", type=str, help="Name of the remote Folder in the sftp server to place the fle into")
parser.add_argument("-c", "--cleanup", type=str, help="Set to true if you want to delete all intermedium files at the end")
parser.add_argument("-d", "--useDB", type=str, help="Set to true if you want to extract data from DB first instead of providing a source file")

args = parser.parse_args()

if args.useDB and args.file and args.folder:
    connect_and_dump_to("SELECT * FROM cars", args.file, r'REG#\[.+\]')
if args.file:
    print(f"Processing src file: {args.file} .....")
if args.folder:
    intFile = strip_pattern_from_csv("1", args.file, args.folder, r'REG#\[.+\]', True)
    
    intFile = strip_pattern_from_csv("2", intFile, args.folder, r'#VIN=.{17}', True)
    
    print(f"Stripping second pattern from intermedium files: {intFile}")
    intFile = strip_pattern_from_csv("3", intFile, args.folder, r'VIN# is .{17}', True)
    intFile = strip_pattern_from_csv("4", intFile, args.folder, r'VIN:.{17}.', True)
    intFile = strip_pattern_from_csv("5", intFile, args.folder, r'VIN Number: .{17}', True)
    intFile = strip_pattern_from_csv("6", intFile, args.folder, r'VIN .{17}', True)
    intFile = strip_pattern_from_csv("7", intFile, args.folder, r'VIN- .{17}', True)
    intFile = strip_pattern_from_csv("8", intFile, args.folder, r'VIN.[ \t].{17}', True)
    
    intFile = strip_pattern_from_csv(args.file, intFile, args.folder, r'VIN is .{17}', False)
    
    
else:
    print("ERROR: Remote sftp folder has not been configured")
if args.cleanup:
    print(f"Cleaning up intermedium files... ")
    i=1
    while i <= 8:
        os.remove(f"{os.path.join(args.folder, f"int.{i}.csv")}")
        i+=1
