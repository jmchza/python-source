# import pandas with shortcut 'pd'
import pandas as pd  
import argparse
import os
import re
import pyodbc
from sqlalchemy import create_engine



def get_connection():
    # Define your connection parameters
    server = os.getenv("SERVER_NAME", "set-me-up-in-env-vars")
    database = os.getenv("SERVER_DB", "set-me-up-in-env-vars")
    #username = os.getenv("SERVER_USER", "username")
    #password = os.getenv("SERVER_PW", "password")
 
    # Create the connection string
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};TrustServerCertificate=yes;Trusted_Connection=yes" ##UID={username};PWD={password};
    # Establish the connection
    connection = pyodbc.connect(connection_string)
    return connection
   
def prepare_create_satement(table_name, headers):
    
        createQuery = f"CREATE TABLE {table_name} ("
        
        for col in headers:
            createQuery = createQuery + f"{col} varchar(255),"
        
        createQuery = createQuery[:-1] + ")"
        
        return createQuery
    
def read_sql_file(file):
    # Open the file in read mode
    file = open(file, "r")

    # Read the entire content of the file
    content = file.read()

    # Close the file
    file.close()
    return content

def strip_and_normalize_headers(headers):
    return [d.replace("/","") for d in [q.replace("6%","") for q in [p.replace("9%", "") for p in [u.replace("?","") for u in [v.replace("20%","_") for v in [r.replace(".", "_") for r in [t.replace("]","") for t in [s.replace("[","") for s in headers]]]]]]]]
    
# Initialize parser
parser = argparse.ArgumentParser(description="Initializing the parser")

parser.add_argument("-n", "--file", type=str, help="Source file to process")
parser.add_argument("-l", "--list", type=str, help="Column list to drop of from original source file, separated by comma.")
parser.add_argument("-f", "--folder", type=str, help="If you want to save it into a file too, please specify a folder to save the file to.")
parser.add_argument("-t", "--table", type=str, help="you need to specify a table to import into, i.e: -t TABLE_NAME")
parser.add_argument("-cs", "--createStatement", type=str, help="To pick uop the create staement from a sql file, uuse -ct parameter with the location of the file to use.")

args = parser.parse_args()

if args.file:
    print(f"Processing src file: {args.file} .....")

# read_csv function which is used to read the required CSV file
data = pd.read_excel(args.file, sheet_name=0)

headers = data.head(0)

# drop function which is used in removing or deleting rows or columns from the CSV files
if args.list:
    print(f"Processing Column list: {args.list} .....")
    for el in args.list.split(","):
        data.pop(el)

df = pd.DataFrame(data)

# display
if args.folder:
    fileLocation = os.path.join(args.folder, args.file.split("/")[-1])
    print(f"Saving file in : {fileLocation} ...")
    
    with pd.ExcelWriter(fileLocation) as writer:
        df.to_excel(writer)
else:
    print("If you want to save it into a file too, please specify a folder to save the file to with parameter -f")
    
headers = df.head(0)

new_headers = [re.sub(" ", "", str(cell)) for cell in [re.sub("-", "_", str(cell)) for cell in [re1.replace("(", "") for re1 in [re.replace(")", "") for re in headers]]]]

createSmt = ""
table = ""
if args.table:
        strippedHeaders = strip_and_normalize_headers(new_headers)
        # print(f"strippedHeaders: {strippedHeaders}")
        createSmt = prepare_create_satement(args.table, strippedHeaders)
else:
    print("You can specify a table to import into, i.e: -t TABLE_NAME or use the -cs parameter to pass a sql file instead.")

if args.createStatement:
    createSmt = read_sql_file(args.createStatement)
    ff = createSmt.split(" ")
    table = ff[2]

vals = []
valsParameters = []
print(f"Inserting records into {table}...")
# strippedHeaders = strip_and_normalize_headers(new_headers)

server = os.getenv("SERVER_NAME", "localhost")
database = os.getenv("SERVER_DB", "temp")
username = os.getenv("SERVER_USER", "username")
password = os.getenv("SERVER_PW", "password")
    
params = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Create the engine
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
try:
    df.to_sql(table, engine, if_exists="replace",index=False)
except Exception as e:
    print(f"Return Code=1 {e}")
    exit()
print("Returned CODE=0")