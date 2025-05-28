import csv
import re
import paramiko
import argparse
import os
import platform

def strip_pattern_from_csv(input_file, output_file, pattern):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            # Apply regex to each cell in the row
            new_row = [re.sub(pattern, '', cell) for cell in row]
            writer.writerow(new_row)


def sftp_upload_file(local_file_path, remote_file_path, hostname, port, username, password):
    # Create an SFTP client
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Upload the file
    try:
        sftp.put(local_file_path, remote_file_path)
    except Exception as ex:
        print(ex)

    # Close the SFTP connection
    sftp.close()
    transport.close()

# SFTP connection details
remote_file_path = '/'
hostname = os.environ.get("SFTP_HOSTNAME", "test.rebex.net") 
port = os.environ.get("SFTP_HOSTNAME", 22) 
username = os.environ.get("SFTP_HOSTNAME", "demo")
password = os.environ.get("SFTP_HOSTNAME", 'password')

# Initialize parser
parser = argparse.ArgumentParser(description="Initializing the parser")

parser.add_argument("-n", "--file", type=str, help="Name of the file to remove REG and VIN from Comments")
parser.add_argument("-f", "--folder", type=str, help="Name of the remote Folder in the sftp server to place the fle into")
parser.add_argument("-c", "--cleanup", type=str, help="Set to true if you want to delete all intermedium files at the end")

args = parser.parse_args()
intermedium_file = 'bmw.int.csv'

if args.file:
    print(f"Processing file: {args.file} .....")
    strip_pattern_from_csv(args.file, intermedium_file, r'REG#\[.+\]')
    file_name = args.file.split(".csv")
    output_file = file_name[0] + '.cleanedup.csv'

    strip_pattern_from_csv(intermedium_file, output_file, r'VIM#\[.+\]')
if args.folder:
    print(f"Copying {output_file} into {args.folder} dir")
    plat = platform.system()
    # sftp_upload_file(f"./{output_file}", remote_file_path, hostname, port, username, password)
    if plat in ["Darwin", "Linux"]:
        os.popen(f"cp {output_file} {args.folder}")
    else:
        os.popen(f"copy {output_file} {args.folder}")
else:
    print("ERROR: Remote sftp folder has not been configured")
if args.cleanup:
    print("Cleaning up intermedium files...")
    os.remove(f"./{intermedium_file}")
