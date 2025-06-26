import re
import argparse
import os
from glob import glob

def get_csv_files(dir_path, filePattern):
    os.chdir(dir_path)
    return list(map(lambda x: os.path.join(dir_path, x), glob(filePattern)))

# Initialize parser
parser = argparse.ArgumentParser(description="Initializing the parser")

parser.add_argument("-n", "--file", type=str, help="Name or file pattern to instruct the process to look up for")
parser.add_argument("-f", "--folder", type=str, help="Folder in which the the files will be cleaned up")
parser.add_argument("-v", "--verbose", type=str, help="Set to true Verbose if you want to see the list of files getting deleted")

args = parser.parse_args()

if args.folder:
    print(f"Remote dir: {args.folder}")
    filesArray = get_csv_files(args.folder, args.file)
    print(filesArray)
    for file in filesArray:
        if args.verbose:
            print(f"Deleting file: {file}")
        # os.remove(file)
else:
    print("ERROR: Remote sftp folder has not been configured")