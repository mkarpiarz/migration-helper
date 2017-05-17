#!/bin/bash
set -x
# Percentage of RAM to be stressed:
RAMPERC=0.4
/bin/echo "Installing stress..."
/usr/bin/sudo /usr/bin/apt-get update
/usr/bin/sudo /usr/bin/apt-get install -y stress
/bin/echo "Running stress..."
/usr/bin/stress --vm-bytes $(/usr/bin/awk -v ramperc=$RAMPERC '/MemFree/{printf "%d\n", $2 * ramperc;}' < /proc/meminfo)k --vm-keep -m 1 &
