# import pandas with shortcut 'pd'
import pandas as pd  
import argparse
import os
import re
import pyodbc

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
    
# Initialize parser
parser = argparse.ArgumentParser(description="Initializing the parser")

parser.add_argument("-n", "--file", type=str, help="")
parser.add_argument("-l", "--list", type=str, help="")
parser.add_argument("-f", "--folder", type=str, help="Folder in which the file will be output to")
parser.add_argument("-t", "--table", type=str, help="")

args = parser.parse_args()

if args.file:
    print(f"Processing src file: {args.file} .....")
if args.list:
    print(f"Processing Column list: {args.list} .....")

# read_csv function which is used to read the required CSV file
data = pd.read_excel(args.file, sheet_name=0)

headers = data.head(0)

# drop function which is used in removing or deleting rows or columns from the CSV files
if args.list:
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
new_headers = [re.sub(" ", "", str(cell)) for cell in [re.sub("-", "_", str(cell)) for cell in headers]]

if args.table:
    
    strippedHeaders = [d.replace("/","") for d in [q.replace("6%","") for q in [p.replace("9%", "") for p in [u.replace("?","") for u in [v.replace("20%","_") for v in [r.replace(".", "_") for r in [l.replace(")","") for l in [t.replace("]","") for t in [s.replace("[","") for s in new_headers]]]]]]]]]
    print(f"strippedHeaders: {strippedHeaders}")
    createSmt = prepare_create_satement(args.table, strippedHeaders)
else:
    print("you need to specify a table to import into, i.e: -t TABLE_NAME")
    exit()

connection = get_connection()

# Create a cursor object
cursor = connection.cursor()

# Execute a query
cursor.execute(createSmt)
connection.commit()

vals = []
valsParameters = []
for i in range(len(df)):
    for j in range(len(df.iloc[i].values)):
        valsParameters.append("%s")
        vals.append(df.iloc[i].values[j])
    
    insertQuery = f"INSERT INTO {args.table} {tuple(list(strippedHeaders))} VALUES {tuple(list(valsParameters))}"
    # print(insertQuery)
    
    if i == 2:
        cursor.execute(insertQuery, vals)
        break

connection.commit()
# Close the connection
connection.close()
# print(data)