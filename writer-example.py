import csv

# Data to be written to the CSV file
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 30, 'New York'],
    ['Bob', 25, 'Los Angeles'],
    ['Charlie', 35, 'Chicago']
]

# Specify the file name
file_name = 'output.csv'

# Open the file in write mode
with open(file_name, mode='w', newline='') as file:
    # Create a CSV writer object
    csv_writer = csv.writer(file)
    
    # Write the data to the CSV file
    csv_writer.writerows(data)

print(f"Data has been written to {file_name}")
