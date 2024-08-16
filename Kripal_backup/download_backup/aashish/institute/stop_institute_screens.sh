#!/bin/bash

# List all screen sessions and filter for those starting with "institute_"
screens=$(screen -ls | grep -o '[0-9]*\.institute_[0-9]*')

# Loop through each screen session
for screen in $screens; do
  # Extract the session name
  session_name=$(echo $screen | cut -d'.' -f2)
  
  # Check if the screen name is not "institute_1" or "institute_5"
  if [[ $session_name != "institute_1" && $session_name != "institute_5" ]]; then
    # Stop the screen session
    echo "Stopping screen session: $screen"
    screen -S "$screen" -X quit
  fi
done
