import csv

# Open the CSV file and create a CSV reader object
with open('data/zone.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Loop through each row in the CSV file
    print("ZONES")
    print("::::::::::::::::::::::::::::::::::::::::::::")
    for row in csvreader:
        # Extract the zone name and member list from the row

        zone_name = row[0]
        members = ",".join(row[1:])
        
        # Generate the Brocade SAN switch commands for the zone
        zone_create_cmd = 'zonecreate "{}";{}'.format(zone_name, members)
        
        # Print the zone creation command to the console
        print(zone_create_cmd)
    print("::::::::::::::::::::::::::::::::::::::::::::")
    print("ZONES")
