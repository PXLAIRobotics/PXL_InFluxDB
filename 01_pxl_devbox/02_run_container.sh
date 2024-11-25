#!/bin/bash

docker run -it --rm -p 80:80 \
       --name `cat ./image_name | cut -d":" -f1` \
       --hostname `cat ./image_name | cut -d":" -f1` \
       -v `pwd`/../Commands/:/home/user/bin \
       -v `pwd`/../App/:/home/user/app/ \
       -v `pwd`/../Test/:/home/user/test \ 
       -v `pwd`/../Data:/home/user/data  \
       -v /etc/localtime:/etc/localtime:ro \
       `cat ./image_name` \
       bash
        
