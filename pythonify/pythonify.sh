#!/bin/bash

wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz

ID=$(($UID - 3000))

cat <<EOF >> ~/.myhosts
10.40.13.151    downstream
10.40.13.1      treatment
10.40.13.66     residential
10.40.13.130    stormdrain
10.40.13.235    pretreatment
EOF

export HOSTALIASES=~/.myhosts

for x in 130 235 1; do
    ssh-copy-id root@10.40.$ID.$x 
    scp Python-3.7.2.tgz root@10.40.$ID.$x:~
    ssh root@10.40.$ID.$x 'tar -zxvf Python-3.7.2.tgz'
    ssh root@10.40.$ID.$x 'cd Python-3.7.2;./configure;make;make install'
done
