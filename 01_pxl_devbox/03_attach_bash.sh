#!/bin/bash

docker exec -it `cat ./image_name | cut -d":" -f1` bash
