#!/usr/bin/bash
nohup python3 main.py </dev/null &>/dev/null &
ps -aux | grep python
echo "Program start!\n"
