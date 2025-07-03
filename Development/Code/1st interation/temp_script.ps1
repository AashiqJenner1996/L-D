
# Get the row count for the original file
$rowCount1 = (Get-Content -Path '*.log').Count

# Get the contents of any log files 
$contents = Get-Content -Path '*.log'

New-Item -Path 'Client' -ItemType 'Directory'


# Create a new file for errors 
New-Item -Path 'ClientErrors.txt' -ItemType 'File'

# Create a new file for warnings 
New-Item -Path 'ClientWarnings.txt' -ItemType 'File'

# Create a new file for errors 
New-Item -Path 'ClientStats.txt' -ItemType 'File'

# Filter the contents of log file to only include lines that contain the word 'error'
$filteredContents = $contents | Select-String -Pattern 'error'

# Write the filtered contents to the file 'b.txt'
Set-Content -Path 'ClientErrors.txt' -Value $filteredContents

# Get the row count for the second file
$rowCount2 = (Get-Content -Path 'ClientErrors.txt').Count


# Filter the contents of log to only include lines that contain the word 'warning'
$filteredContents = $contents | Select-String -Pattern 'warning'

# Write the filtered contents to the file 'b.txt'
Set-Content -Path 'ClientWarnings.txt' -Value $filteredContents

# Get the row count for the second file
$rowCount3 = (Get-Content -Path 'ClientWarnings.txt').Count

# Close the log file 
Out-File -FilePath '*.log' -OutputMode Append -NoClobber


# Calculate the percentage difference in row count
$percentageDifferenceErrors = (($rowCount2) / $rowCount1) * 100
$percentageDifferenceWarnings = (($rowCount3) / $rowCount1) * 100

# Display the percentage difference in row count
Write-Host "The error percentage is $percentageDifferenceErrors%."
Write-Host "The warning percentage is $percentageDifferenceWarnings%."

Set-Content -Path 'ClientStats.txt' -Value "Errors: $percentageDifferenceErrors% & Warnings: $percentageDifferenceWarnings%"

Move-Item -Path $filePath -Destination 'Client'
Move-Item -Path 'ClientWarnings.txt' -Destination 'Client'
Move-Item -Path 'ClientErrors.txt' -Destination 'Client'
Move-Item -Path 'ClientStats.txt' -Destination 'Client' 
