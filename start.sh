#!/bin/bash

ID=$(($UID - 3000))

for box in 130 235 1 66; do
    ssh root@10.40.$ID.$box $1
done