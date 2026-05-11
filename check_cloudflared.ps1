```powershell
# Define the directories to search
$directories = @("C:\Program Files (x86)\cloudflared\", "C:\Program Files\cloudflared\")

# Initialize a variable to store the result
$result = $null

# Loop through each directory and check for cloudflared
foreach ($dir in $directories) {
    if (Test-Path -Path "$dir\cloudflared.exe") {
        $result = "Cloudflared found at: $dir"
        break
    }
}

# Output the result
if ($result) {
    Write-Output $result
} else {
    Write-Output "Cloudflared not found in specified directories."
}
```
