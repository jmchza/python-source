# Clean up REG and VIN fields from field Comments from bmw and mini csv files or DB

## SETUP 
Once you the venv environemt has been created and before you are able to run the right command you need to set the folowing environment variables:

On Linux
```
export FTP_HOSTNAME=test.rebex.net
export SFTP_HOSTNAME=22 
export SFTP_HOSTNAME=demo
export SFTP_HOSTNAME=password
```

On Windows
```
set FTP_HOSTNAME=test.rebex.net
set SFTP_HOSTNAME=22 
set SFTP_HOSTNAME=demo
set SFTP_HOSTNAME=password
```


## To run the script

> Parametters
* -n Name of the file to remove REG and VIN from Comments
* -f Name of the remote Folder in the sftp server to place the fle into
* -c Set to true if you want to delete all intermedium files at the end
* -d Set to true if you want to extract data from DB first instead of providing a source file

NOTE: if you specify a DB to use as a source of data, you sill need to provide a file name which is going tobe used to save that extracted data to.

```
python cleanup-comments.py -n bmw.csv -f ./tmp -c true 
```


Output i.e: 
```
Processing file: bmw.csv .....
Copying bmw.cleanedup.csv into sftp folder
Remote dir: /
[Errno 13] Access denied.
```

# Delete old enquiry data files from specified folder

> Parametters
* -n fName or file pattern to instruct the process to look up for 
* -f Folder in which the the files will be cleaned up
* -v true to sert to verbose


```
clean-up-old-files.py -n '*.csv' -f ./ -v true
```

Output with verbosity activated i.e: 
```
Remote dir: ./
['./bmw.csv', './bmw.int.csv', './bmw.cleanedup.csv']
Deleting file: ./bmw.csv
Deleting file: ./bmw.int.csv
Deleting file: ./bmw.cleanedup.csv
```

# To drop of colummns from a excel file.

* ON Linux
```
python drop-customer-fields-2294.py -n ./srcFiles/020_IVS_Registrations_Order_Analysis.xlsx  -l "Contact Name,Business Contact - End User Address Line 1,Business Contact - End User Address Line 2,Business Contact - End User Address Line 3,Business Contact - End User Town,Business Contact - End User County,Business Contact - End User Postcode,Purchaser Name,Business Contact - Purchaser Address Line 1,Business Contact - Purchaser Address Line 2,Business Contact - Purchaser Address Line 3,Business Contact - Purchaser Town,Business Contact - Purchaser County,Business Contact - Purchaser Postcode,Vehicle Detail - First Reg Keeper Name,Vehicle Detail - Reg Keeper Name"
```

* On Winows 

```
python drop-customer-fields-2294.py -n .\srcFiles\020_IVS_Registrations_Order_Analysis.xlsx  -l "Contact Name,Business Contact - End User Address Line 1,Business Contact - End User Address Line 2,Business Contact - End User Address Line 3,Business Contact - End User Town,Business Contact - End User County,Business Contact - End User Postcode,Purchaser Name,Business Contact - Purchaser Address Line 1,Business Contact - Purchaser Address Line 2,Business Contact - Purchaser Address Line 3,Business Contact - Purchaser Town,Business Contact - Purchaser County,Business Contact - Purchaser Postcode,Vehicle Detail - First Reg Keeper Name,Vehicle Detail - Reg Keeper Name"
```

