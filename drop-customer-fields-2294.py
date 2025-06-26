# import pandas with shortcut 'pd'
import pandas as pd  
import argparse
import os

# Initialize parser
parser = argparse.ArgumentParser(description="Initializing the parser")

parser.add_argument("-n", "--file", type=str, help="")
parser.add_argument("-l", "--list", type=str, help="")
parser.add_argument("-f", "--folder", type=str, help="Folder in which the file will be output to")

args = parser.parse_args()

if args.file:
    print(f"Processing src file: {args.file} .....")
if args.list:
    print(f"Processing Column list: {args.list} .....")

# read_csv function which is used to read the required CSV file
data = pd.read_excel(args.file, sheet_name=0)

print("Before")
print(data)

# drop function which is used in removing or deleting rows or columns from the CSV files
if args.list:
    for el in args.list.split(","):
        data.pop(el)
        # print("After iteration")
        print(data)

# display
if args.folder:
    print(f"Saving file in : {os.path.join(args.folder, args.file.split("/")[-1])} ...")
    # pd.to_excel(f"{ os.path.join(args.folder, args.file)}")
    df = pd.DataFrame(data)
    
    with pd.ExcelWriter(f"{os.path.join(args.folder, args.file.split("/")[-1])}") as writer:
        df.to_excel(writer, sheet_name="Order Analysis")
else: 
    print("File has not been saved, please specify a folder to save the file to.")
print(data)