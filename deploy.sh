#!/bin/bash

ID=$(($UID - 3000))

if [ "$#" -eq 0 ]; then
    for box in 130 235 1 66; do
        for file in $(ls); do
            scp $file root@10.40.$ID.$box:~
        done
    done
elif [ "$#" -eq 1 ]; then
    for box in 130 235 1 66; do
        scp $1 root@10.40.$ID.$box:~
    done
else
    echo "Unknown options"
fi


