#!/bin/bash

ID=$(($UID - 3000))
wget https://miravalier.net/build-essential.tar.gz
scp build-essential.tar.gz root@10.40.$ID.66:
ssh root@10.40.$ID.66 'tar -xvzf build-essential.tar.gz;cd build-essential;dpkg -i $(ls)'
