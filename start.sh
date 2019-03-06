#!/bin/bash

ID=$(($UID - 3000))
command=$1

for box in 130 235 1 66; do
    scp root@10.40.$ID.$box $command
done