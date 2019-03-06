#!/bin/bash

wget https://www.github.com/secdev/scapy/archive/v2.4.2.tar.gz
ID=$(($UID - 3000))

for x in 130 235 1 66; do
    scp -r v2.4.2.tar.gz root@10.40.$ID.$x:
    ssh root@10.40.$ID.$x 'tar -zxvf v2.4.2.tar.gz'
    ssh root@10.40.$ID.$x 'cd scapy-2.4.2;python3 ./setup.py install'
done