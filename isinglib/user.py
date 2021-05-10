import os
import sys
import numpy as np


def default_options():
    opts={}
    opts['seed'] = None
    opts['extfield'] = 0
    opts['nstep'] = 100
    opts['nspazzate'] = 1
    opts['rngstatus'] = None
    opts['bmax'] = None
    opts['unitx'] = 'n'
    opts['grain'] = 0.01
    opts['oss'] = 'amag'
    opts['out_file'] = None
    return opts


def user_query(def_opts):
    supp_opts = ('binder','chi','amag','mag','c','ene')
    opts = def_opts.copy()
    opts['L'] = int(input('Insert lattice (LxL) dimension \nL = '))
    temp = input("Default temperature unit: beta=1/T. Change into T? Y/N ").lower()
    opts['unitx'] = temp == '' and 'n' or temp
    temp = input('Insert observable(s) between ' + ','.join(supp_opts) + ': ').strip().replace(';',',').split(',')
    opts['oss'] = set(temp) <= set(supp_opts) and temp or None
    opts['beta'] = float(input('Insert initial temperature: '))
    if opts != None:
        opts['bmax'] = float(input('Insert final temperature: '))
        temp = input('Insert temperature step: ')
        if temp:
            opts['grain'] = float(temp)
    temp = input('Insert number of MonteCarlo iterations (1 iter -> 1 lattice update): ')
    if temp:
        opts['nstep'] = int(temp)
    temp = input('Insert external field strength (default=0): ')
    if temp:
        opts['extfield'] = float(temp)

    return opts