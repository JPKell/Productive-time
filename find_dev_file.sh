#!/bin/bash

# This till search the hidraw devices and return the dev file for the eMetuM device

FILES=/dev/hidraw*
for f in $FILES
do
  FILE=${f##*/}
  DEVICE="$(cat /sys/class/hidraw/${FILE}/device/uevent | grep HID_NAME | cut -d '=' -f2)"
    if [ "$DEVICE" == "muteme.com MuteMe" ]; 
    then
        printf "%s" $FILE
    fi  
done
