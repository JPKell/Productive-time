#! /bin/bash

# This will be used to change the settings on the device. 


# Check if $2 is a string and if it is, then use it as the device file
if [ -z "$2" ]; then
    dev=$(./find_dev_file.sh)
else
    dev=$2
fi

# Check if $1 is a string and if it is, then use it as the device file
if [ -z "$1" ]; then
    echo "No command given"
    exit 1
fi
echo -e $1 > /dev/$dev
 