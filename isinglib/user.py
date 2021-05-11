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
    opts['path'] = os.curdir
    opts['take_storie'] = True
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
    temp = input('Insert observable(s) between ' + ', '.join(supp_opts) + ': ').lower().replace(',',' ')
    res = set( temp.split() )
    if not( ( res <= set(supp_opts) )  and  res):
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
    msg = 'Step along temperature axis [default: {:.3f}]: '
    temp = input(msg.format(opts['grain']))
    if temp:
        try:
            opts['grain'] = float(temp)
            if opts['grain'] <= 0:
                raise errors.OptionError('Step along temperature axis\nStep along temperature axis must be a positive float')
        except ValueError:
            raise errors.OptionError('Step along temperature axis\nStep along temperature axis must be a positive float')
    #extfield
    msg = 'Insert external field strength [default: {:.2f}]: '
    temp = input(msg.format(opts['extfield']))
    if temp:
        try:
            opts['extfield'] = float(temp)
        except ValueError:
            raise errors.OptionError('External field strength\nExternal field strength must be a float')
        
    temp = input('Insert number of MonteCarlo iterations (1 iter -> 1 lattice update): [default: {}]\n'.format(opts['nstep']))
    if temp:
        try:
            opts['nstep'] = int(temp)
            if opts['nstep'] <= 0:
                raise errors.OptionError('number of step MonteCarlo iterations\nNumber of Step MonteCarlo iterations must be a positive integer')
        except ValueError:
             raise errors.OptionError('number of step MonteCarlo iterations\nNumber of Step MonteCarlo iterations must be a positive integer')
    
    temp = input('Insert random number generator seed: [default: {}]\n'.format(opts['seed']))
    if temp:
        try:
            opts['seed'] = int(temp)
            if opts['seed'] <= 0:
                raise errors.OptionError('seed\nSeed must be a positive integer')
        except ValueError:
             raise errors.OptionError('seed\nSeed must be a positive integer')
    save = input('Save the results? If yes, insert path [default: {}] . If no, insert N\n'.format(os.path.abspath(os.curdir))).strip()
    if save.lower()!='n':
        flag = True
        while flag:
            if save:
                if os.path.exists(save):
                    flag=False
                    opts['path']=save
                else:
                    flag2 = True
                    while flag2:
                        i = input('{} directory does not exist. Create? Y/N\n'.format(save) ).lower().strip()
                        if i == 'y':
                            try:
                                os.mkdir(save)
                                opts['path'] = save
                                flag2 = False
                                flag = False
                            except FileNotFoundError:
                                raise errors.OptionError('path\nWrong input path %s'%save)
                        elif i == 'n':
                            flag2=False
                            save = input('Insert path [default: {}]\n'.format(os.path.abspath(os.curdir) )).strip()
                        else:
                            print('Not understood, try again.')
                            
            else:
                flag = False
                opts['path']=os.curdir
                
                
        opts['out_file'] = '{}_L{}_lb{:.2f}'.format('_'.join(opts['oss']),opts['L'],opts['beta_lower'])
        fmt = 'Insert output file (txt) name [default: {}]\n'.format( opts['out_file'] )
        flag = True
        while flag:
            temp = input(fmt).strip().split('.txt')[0]
            res = opts['out_file']
            if temp:
                res = temp
            else:
                fmt = 'Insert output file (txt) name [default already exist]\n'
            if os.path.exists(opts['path']+os.sep+res+os.extsep+'txt'):
                flag2 =True
                while flag2:
                    i=input('{} does already esist. Overwrite? Y/N\n'.format(res+os.extsep+'txt')).lower().strip()
                    if i=='y':
                        flag = False
                        flag2 = False
                    elif i=='n':
                        print('Choose a different file name')
                        flag2 = False
                    else:
                        print('Not understood, try again.')
            else:
                flag=False
        opts['out_file'] = res + os.extsep + 'txt'
    else:
        opts['path']=None
        opts['out_file'] = None
    while True:
        temp = input('Save (into the directory ''L={}'') MonteCarlo stories to enhance future simulations? Y/N [default: Y]\n'.format(opts['L']) ).lower().strip()
        if temp in ['y',''] :
            opts['save_storie'] = True
            if 'L={}'.format(opts['L']) not in os.listdir(os.curdir):
                opts['take_storie'] = False
                os.mkdir('L={}'.format(opts['L']))
                print('Directory L={} created'.format(opts['L']) )
            break
        elif temp == 'n':
            opts['save_storie'] = False
            break
        else:
            print('Not understood, try again.')
    
            
                    
    return opts




