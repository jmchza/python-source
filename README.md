# Clean up REG and VIN fields from field Comments from bmw and mini csv files

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
* -n file to process 
* -f remotePAth to sftp server

```
python cleanup-comments.py -n bmw.csv -f /
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