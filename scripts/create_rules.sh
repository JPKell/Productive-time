#!/bin/sh

# This must be run as sudo!

# Device low level support is handled by the kernel, but is managed in userspae by udev.
# udev is a daemon that monitors the kernel for device events and runs rules to set 
# permissions and ownership of devices. 

cd /etc/udev/rules.d/
# Create the file if it doesn't exist
touch emetum.rules
# Wipe the file
> emetum.rules
# Add the rules
echo 'SUBSYSTEM=="input", GROUP="input", MODE="0666"' >> emetum.rules
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="20a0", ATTRS{idProduct}=="42da", MODE:="666", GROUP="plugdev"' >> emetum.rules
echo 'KERNEL=="hidraw*", ATTRS{idVendor}=="20a0", ATTRS{idProduct}=="42da", MODE="0666", GROUP="plugdev"' >> emetum.rules

echo 'SUBSYSTEM=="input", GROUP="input", MODE="0666"' >> emetum.rules
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="20a0", ATTRS{idProduct}=="42db", MODE:="666", GROUP="plugdev"' >> emetum.rules
echo 'KERNEL=="hidraw*", ATTRS{idVendor}=="20a0", ATTRS{idProduct}=="42db", MODE="0666", GROUP="plugdev"' >> emetum.rules
# Reload the rules
udevadm control --reload-rules
udevadm trigger

echo 'Registred eMetuM device'