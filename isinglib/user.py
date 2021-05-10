import os
import sys
import numpy as np
from isinglib import errors


def default_options():
    opts={}
    opts['seed'] = None
    opts['rngstatus'] = None
    opts['extfield'] = 0
    opts['nstep'] = 100
    opts['nspazzate'] = 1
    opts['out_file'] = None
    return opts


def user_query(def_opts):
    supp_opts = ('binder','chi','amag','mag','c','ene')
    opts = def_opts.copy()
    temp = input('Insert lattice (LxL) dimension \nL = ')
    try:
        opts['L'] = int(temp)
        if opts['L'] <= 0:
            raise errors.OptionError('L\nL must be a positive integer')
    except ValueError:
        raise errors.OptionError('L\nL must be a positive integer')
    #observables
    temp = input('Insert observable(s) between ' + ', '.join(supp_opts) + ': ').strip().replace(';',',')
    res = set( temp.replace(' ','').split(',') )
    if not ( res <= set(supp_opts) ):
        raise errors.OptionError('observable(s)\nObservable(s) must be at least one between '+ ', '.join(supp_opts))
    opts['oss'] = list( res )
    #temperature
    temp = input('Default temperature unit: beta=1/T. Change into T? Y/N [default: N]\n').lower()
    opts['unitx'] , opts['grain'] = (temp.strip() == '') and ('n', 0.01) or ('y', 0.2)
    temp = input('Insert lower temperature: ')
    try:
        opts['beta_lower'] = float(temp)
        if opts['beta_lower'] < 0:
            raise errors.OptionError('lower temperature\nThe temperature must be a non-negative float')
    except ValueError:
        raise errors.OptionError('lower temperature\nThe temperature must be a non-negative float')
    temp = input('Insert upper temperature: ')
    try:
        opts['beta_upper'] = float(temp)
        if opts['beta_upper'] < 0:
            raise errors.OptionError('upper temperature\nThe temperature must be a non-negative float')
    except ValueError:
        raise errors.OptionError('upper temperature\nThe temperature must be a non-negative float')
    if opts['beta_lower'] > opts['beta_upper']:
        print('Lower and upper temperatures inverted.  Correcting.')
        opts['beta_lower'], opts['beta_upper'] = opts['beta_upper'], opts['beta_lower']
    msg = 'Step along temperature axis (default: {:.3f}): '
    temp = input(msg.format(opts['grain']))
    if temp:
        try:
            opts['grain'] = float(temp)
            if opts['grain'] <= 0:
                raise errors.OptionError('Step along temperature axis\nStep along temperature axis must be a positive float')
        except ValueError:
            raise errors.OptionError('Step along temperature axis\nStep along temperature axis must be a positive float')
    #extfield
    msg = 'Insert external field strength (default: {:.2f}): '
    temp = input(msg.format(opts['extfield']))
    if temp:
        try:
            opts['extfield'] = float(temp)
        except ValueError:
            raise errors.OptionError('External field strength\nExternal field strength must be a float')
        
    temp = input('Insert number of MonteCarlo iterations (1 iter -> 1 lattice update): [default: {}]\n '.format(opts['nstep']))
    if temp:
        try:
            opts['nstep'] = int(temp)
            if opts['nstep'] <= 0:
                raise errors.OptionError('number of step MonteCarlo iterations\nNumber of Step MonteCarlo iterations must be a positive integer')
        except ValueError:
             raise errors.OptionError('number of step MonteCarlo iterations\nNumber of Step MonteCarlo iterations must be a positive integer')
    
    temp = input('Insert random number generator seed: [default: {}]\n '.format(opts['seed']))
    if temp:
        try:
            opts['seed'] = int(temp)
            if opts['seed'] <= 0:
                raise errors.OptionError('seed\nSeed must be a positive integer')
        except ValueError:
             raise errors.OptionError('seed\nSeed must be a positive integer')
    
    return opts
