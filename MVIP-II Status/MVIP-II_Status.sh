#!/bin/bash

username="mvip"
device="172.16.179.211"
SSH_Port=22

ssh -t -p "$SSH_Port" "$username@$device" bash <<'EOF'
    checkStatus() {
        for card in "${cards[@]}"; do
            if ping -c 4 $card >/dev/null 2>&1; then
                echo "Ping to $card was successful."
            else
                echo "Ping to $card was unsuccessful."
            fi
            echo "-----------------------------------"
        done
    }
# add more to the list if required.
cards=(
    "172.16.179.212"
    "172.16.179.213"
    "172.16.179.214"
    "172.16.179.215"
    "172.16.179.216"
    "172.16.179.217"
    "172.16.179.221"
    "172.16.179.223"
)

checkStatus
EOF

echo "Ping operations completed."