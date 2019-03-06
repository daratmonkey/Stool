#!/bin/bash

ID=$(($UID - 3000))

for box in 130 235 1 66; do
    for file in .; do
        scp $file root@10.40.$ID.$box:~
    done
done
