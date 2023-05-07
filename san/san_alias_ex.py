import csv

# Open the CSV file and create a CSV reader object
with open('alias.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Loop through each row in the CSV fileprint("ALIASES")
    print("ALIASES")
    print("::::::::::::::::::::::::::::::::::::::::::::")
    for row in csvreader:
        # Extract the alias name and member list from the row
        alias_name = row[0]
        members = ",".join(row[1:])
        
        # Generate the Brocade SAN switch commands for the alias
        alias_create_cmd = 'alicreate "{}";{}'.format(alias_name, members)
        
        # Print the alias creation command to the console
        print(alias_create_cmd)