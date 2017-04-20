#!/bin/sh
cd ~/synced_folder/finaldesign/
for i in $( seq 1 35)
do
    # 1000个并发连接
    python client/tcpclient01.py 192.168.10.102:10010 --typeid 1 --delay 0 --num-task 1000 &
    # echo 'hello world'${i}
done

