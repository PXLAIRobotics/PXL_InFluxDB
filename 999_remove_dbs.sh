#!/bin/bash

read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo rm -rf Data/
    sudo rm -rf InfluxDB
fi