#!/bin/bash

(cd ./01_pxl_devbox; ./01_build_image.sh)
(cd ./02_influxdb; ./01_build_image.sh)