
#!/bin/bash

# for debugging
# set -x

# Define a variable of the IP address for your device
device="172.16.176.136"

# this is ID for the element
varID="129@s"
username='mvx'



# fetching the content from webpage
curl -s 'https://172.16.176.136/manage-settings.php' -o page.html

# Parse the HTML and extract the dropdown values
xmllint --html --xpath '//select[@id="dropdown-id"]/option/@value' page.html 2>/dev/null




function remote_commands (){
  expected_status=200
  # Headers (for e.g., Content-Type, Authorization)
  # headers="-H 'Content-Type: application/json' -H 'Authorization: Bearer YourTokenHere'"
  
  declare -a routes=(
    "v.api/apis/EV/SUMMARY"
    "v.api/apis/EV/GET/parameter?varid=$varID" 
    "v.api/apis/EV/GET/parameter/$varID"
    "v.api/apis/EV/SET/parameter?$varID=test" 
    "v.api/apis/EV/SET/parameter/$varID/test"
    "v.api/apis/PT/SUMMARY"
    "v.api/apis/RT/SUMMARY"
  )
  for route in "${routes[@]}"; do 
    url="https://${device}:/${route}"
    echo $url  
    # Making the API call
    response=$(wget --no-check-certificate --server-response --spider "$url" 2>&1 | grep 'HTTP/' | awk 'NR==1 {print $2}')
    if [ "$response" -eq "$expected_status" ]; then
      echo "Test successful for $url (Expected: $expected_status, Got: $response)"
    else
      echo "Test failed for $url (Expected: $expected_status, Got: $response)"
    fi
  done
}
export device
export varID
export -f remote_commands

# making the connection to the server
ssh -t $username@$device "$(declare -p device varID); $(typeset -f remote_commands); remote_commands"
