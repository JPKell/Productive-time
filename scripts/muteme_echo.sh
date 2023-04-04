#! /bin/bash

# Check if $1 is a string and if it is, then use it as the command to send
if [ -z "$1" ]; then
    echo "No command given"
    exit 1
fi

# Check if $2 is a string and if it is, then use it as the device file
# Otherwise, use the find_dev_file.sh script to find the device file
if [ -z "$2" ]; then
    dev=$(./find_dev_file.sh)
else
    dev=$2
fi

echo -e $1 > /dev/$dev
 