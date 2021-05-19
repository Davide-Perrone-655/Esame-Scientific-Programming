#!/usr/bin/env python3

import subprocess as sp

proc_name = 'python3 ising.py '
load_arg =  '-load ourbench.txt'
load_arg1 = '-i'
load_arg2 = '-L 3 -b 0.3 -oss amag -bf 0.4 -n 10 -s 4 -file n -no_save'

res = sp.run(proc_name + load_arg2, shell=True)
print(res)


