import os
import sys
import numpy as np
from isinglib import errors
#import errors
import argparse


def basic_options():
    opts={}
    opts['seed'] = None
    opts['rngstatus'] = None
    opts['extfield'] = 0
    opts['nstep'] = 100
    opts['nspazzate'] = 1
    opts['path'] = os.curdir
    opts['take_storie'] = True
    return opts


def user_save(opts, user=False):
    if user:
        save = input('Save the results? If yes, insert path [default: {}] . If no, insert N\n'.format(os.path.abspath(os.curdir))).strip()
        opts['path'] = save == '' and os.curdir or save

    if opts['path'].lower()!='n':
        flag = True
        while flag:
            if os.path.exists(opts['path']):
                flag=False
            else:
                flag2 = True
                while flag2:
                    i = input('{} directory does not exist. Create? Y/N\n'.format(opts['path']) ).lower().strip()
                    if i == 'y':
                        try:
                            os.mkdir(opts['path'])
                            flag2 = False
                            flag = False
                        except FileNotFoundError:
                            raise errors.OptionError('path\nWrong input path %s'%opts['path'])
                    elif i == 'n':
                        flag2=False
                        save = input('Insert path [default: {}]\n'.format(os.path.abspath(os.curdir) )).strip()
                        opts['path'] = save == '' and os.curdir or save
                    else:
                        print('Not understood, try again.')
        
        
        flag = True
        default_name = '{}_L{}_h{:.2f}'.format('_'.join(opts['oss']),opts['L'],opts['extfield'])
        fmt = 'Insert output file (txt) name [default: {}]\n'.format( default_name )
        user2 = user
        while flag:
            if user2:
                opts['out_file'] = input(fmt).strip().split('.txt')[0]

            if not opts['out_file']:
                fmt = 'Insert output file (txt) name [default already exist]\n'

            opts['out_file'] = opts['out_file'] == '' and default_name or opts['out_file']

            
            if os.path.exists(opts['path']+os.sep+opts['out_file']+os.extsep+'txt'):
                flag2 =True
                while flag2:
                    i=input('{} does already esist. Overwrite? Y/N\n'.format(opts['out_file']+os.extsep+'txt')).lower().strip()
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
            user2 = True
        
        opts['out_file'] = opts['out_file'] + os.extsep + 'txt'
    else:
        opts['path']=None
        opts['out_file'] = None

    if user:
        while True:
            temp = input('Save (into the directory ''{}L={}'') MonteCarlo stories to enhance future simulations? Y/N [default: Y]\n'.format(os.curdir+os.sep+'MC_stories'+os.sep , opts['L']) ).lower().strip()
            if temp in ['y',''] :
                opts['save_storie'] = True
                break
            elif temp == 'n':
                opts['save_storie'] = False
                break
            else:
                print('Not understood, try again.')

    if opts['save_storie']:
        if 'MC_stories' not in os.listdir(os.curdir):
            os.mkdir('MC_stories')
            print('Directory MC_stories created')
        if 'L={}'.format(opts['L']) not in os.listdir(os.curdir+os.sep+'MC_stories'):
            opts['take_storie'] = False
            os.mkdir(os.curdir+os.sep+'MC_stories'+os.sep+'L={}'.format(opts['L']) )
            print('Directory L={} created'.format(opts['L']) )
            
    return opts


def set_options(prog_name, args, supp_opts, usage_msg):
    opt_keys=['load', 'i', 'seed', 'rngstatus', 'extfield', 'nstep', 'nspazzate', 'path', 'L', 'oss', 'unitx', 'grain', 'beta_lower', 'beta_upper', 'out_file', 'save_storie']
    options={}

    parser=argparse.ArgumentParser(prog_name, usage=usage_msg)
    parser.add_argument('-i', action='store_true', help='Interactive mode' )
    parser.add_argument('-L', help='Lattice (LxL) dimension (REQUIRED IF NOT LOADED)', type = int)
    parser.add_argument('-oss', nargs='+', help='Observable(s) to calculate (REQUIRED IF NOT LOADED)', choices=supp_opts)
    parser.add_argument('-b', '--beta_lower', help='Starting beta (1/T) or T value (REQUIRED IF NOT LOADED)', type = float)
    parser.add_argument('-bf', '--beta_upper', help='Final beta value (1/T) or T', type=float)
    parser.add_argument('-u', '--unitx', help='Y changes the x values in T instead of beta, default=N', choices=('y','n','Y','N'), default='n')
    parser.add_argument('-gr', '--grain', type=float, help='Temperature step, default for T: 0.2, default for beta: 0.01')
    parser.add_argument('-hext', '--extfield', help='External field', type=float, default=0)
    parser.add_argument('-n', '--nstep', type=int, help='Number of datas measured from lattice evolution in a single temperature value', default=100)
    parser.add_argument('-s', '--seed', help='Simulation seed', type = int)
    parser.add_argument('-file', '--out_file', help='Output filename. If nothing given, a standard filename will be given', default='')
    parser.add_argument('-p', '--path', help="Output file path. If 'n' given, datas will not be saved ", default = os.curdir)
    parser.add_argument('-saves', '--save_storie', type=bool, help='Save MonteCarlo stories, default True', default=True)
    parser.add_argument('-load', nargs='?', help='Load simulation parameters from file')
    opts = parser.parse_args(args)
    
    if not args:
        parser.print_help()
        return options
    
    if opts.load:
        opts = file_opts(opts.load, opts, opt_keys)


    for keys in opt_keys[2:]:
        options[keys] = getattr(opts, keys, None)

    #print(options)

    if opts.i:
        return user_query(basic_options(), supp_opts=supp_opts)

    

    if options['beta_upper'] == None:
        options['beta_upper']=options['beta_lower']
    
    options['take_storie'] = True
    options['rngstatus'] = None

    if options['grain'] == None:
        if options['unitx'] == 'y' or options['unitx'] == 'y':
            options['grain'] = 0.2
        else:
            options['grain'] = 0.01

    return user_save(options)




def user_query(def_opts, supp_opts):
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
            
    user_save(opts, True)
    print(opts.keys())
    return opts




def file_opts(file_name, opts, opt_keys):
    int_arg = ['L','seed','nstep','nspazzate']
    float_arg = ['beta_lower', 'beta_upper', 'grain', 'extfield']
    bool_arg = ['save_storie']
    file1 = open(file_name, 'r')
    for line in file1:
        temp = line.replace(' ','').strip().split('=')
        if temp[0] in opt_keys:
            if temp[0] in int_arg:
                setattr(opts, temp[0], int(temp[1]))
            elif temp[0] in float_arg:
                setattr(opts, temp[0], float(temp[1]))
            elif temp[0] in bool_arg:
                setattr(opts, temp[0], bool(temp[1]))
            elif temp[0] == 'oss':
                setattr(opts, temp[0], [temp[1]])
            else:
                setattr(opts, temp[0], temp[1])
    
    file1.close()
    return opts






if __name__ == '__main__':
    keys=[]
    opts=set_options(sys.argv[0], sys.argv[1:],'ciao')
    print(opts)




'''

def user_query2(def_opts, supp_opts):
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
                
                
        opts['out_file'] = '{}_L{}_h{:.2f}'.format('_'.join(opts['oss']),opts['L'],opts['extfield'])
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
        temp = input('Save (into the directory ''{}L={}'') MonteCarlo stories to enhance future simulations? Y/N [default: Y]\n'.format(os.curdir+os.sep+'MC_stories'+os.sep , opts['L']) ).lower().strip()
        if temp in ['y',''] :
            opts['save_storie'] = True
            if 'MC_stories' not in os.listdir(os.curdir):
                os.mkdir('MC_stories')
                print('Directory MC_stories created')
            if 'L={}'.format(opts['L']) not in os.listdir(os.curdir+os.sep+'MC_stories'):
                opts['take_storie'] = False
                os.mkdir(os.curdir+os.sep+'MC_stories'+os.sep+'L={}'.format(opts['L']) )
                print('Directory L={} created'.format(opts['L']) )
            break
        elif temp == 'n':
            opts['save_storie'] = False
            break
        else:
            print('Not understood, try again.')
    
            
    print(opts.keys())
    return opts
'''