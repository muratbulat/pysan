# Import the Active Directory module
Import-Module ActiveDirectory

# Path to the file containing the list of VMs
$vmList = Get-Content -Path "C:\path\to\vm_list.txt"

# Initialize a hashtable to store group memberships by department
$departmentGroups = @{}

foreach ($vm in $vmList) {
    try {
        # Get the logged-in user information from the VM
        $user = Get-WmiObject -Class Win32_ComputerSystem -ComputerName $vm | Select-Object -ExpandProperty UserName
        
        if ($user) {
            # Split the domain and username if needed
            $usernameParts = $user.Split('\')
            $username = if ($usernameParts.Length -eq 2) { $usernameParts[1] } else { $user }

            # Get the user's AD information, including department and group memberships
            $adUser = Get-ADUser -Identity $username -Property Department, MemberOf

            if ($adUser) {
                $department = $adUser.Department
                
                # Ensure the department is in the hashtable
                if (-not $departmentGroups.ContainsKey($department)) {
                    $departmentGroups[$department] = @{}
                }
                
                # Iterate through the groups the user is a member of
                foreach ($group in $adUser.MemberOf) {
                    # Resolve the group name from the DistinguishedName
                    $groupName = (Get-ADGroup $group).Name
                    
                    # Initialize or increment the group count for this department
                    if (-not $departmentGroups[$department].ContainsKey($groupName)) {
                        $departmentGroups[$department][$groupName] = 1
                    } else {
                        $departmentGroups[$department][$groupName]++
                    }
                }
            }
        }
    } catch {
        Write-Error "Error processing VM $vm: $($_.Exception.Message)"
    }
}

# Convert the hashtable to an array of objects for easier sorting and filtering
$results = @()
foreach ($department in $departmentGroups.Keys) {
    foreach ($group in $departmentGroups[$department].Keys) {
        $results += [PSCustomObject]@{
            Department = $department
            GroupName  = $group
            UserCount  = $departmentGroups[$department][$group]
        }
    }
}

# Sort the results by department and user count, then group by department
$sortedResults = $results | Sort-Object Department, -Property UserCount -Descending

# Export the results to a CSV file
$outputFile = "C:\path\to\DepartmentGroupCounts.csv"
$sortedResults | Export-Csv -Path $outputFile -NoTypeInformation

Write-Output "Group counts by department have been exported to $outputFile"
