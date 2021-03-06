#!/usr/bin/env python3

''' Users functions'''

from isinglib import ising_errors as errors
from isinglib import ising_small as sml
from isinglib import ising_type
import typing as tp
import argparse
import sys
import os


def set_options(prog_name: str, args: tp.List[str], supp_opts: tp.List[str], usage_msg: str) -> ising_type.tpopt:
    '''Function to set parsed options from ArgParse or from file or from interactive mode'''
    opt_keys=['load', 'i', 'seed', 'rngstatus', 'extfield', 'nstep', 'path', 'L', 'oss', 'unitx', 'grain', 'beta_lower', 'beta_upper', 'out_file', 'save_storie','mod']
    options={}

    parser=argparse.ArgumentParser(prog_name, usage=usage_msg)
    parser.add_argument('-i', action='store_true', help='Interactive mode' )
    parser.add_argument('-L', help='Lattice (LxL) dimension (REQUIRED IF NOT LOADED)', type = int)
    parser.add_argument('-b', '--beta_lower', help='Starting beta (1/T) or T value (REQUIRED IF NOT LOADED)', type = float)
    parser.add_argument('-bf', '--beta_upper', help='Final beta value (1/T) or T', type=float)
    parser.add_argument('-oss', nargs='+', help='Observable(s) to calculate. Insert all if you want all the observables. If nothing, only MC stories will be saved', choices=supp_opts + ['all'], default=[])
    parser.add_argument('-u', '--unitx', help='Y changes the x values in T instead of beta, default=N', choices=('y','n','Y','N'), default='n')
    parser.add_argument('-gr', '--grain', type=float, help='Temperature step (minimum for beta: 0.0001, minimum for T: 0.001), default for T: 0.2, default for beta: 0.01')
    parser.add_argument('-hext', '--extfield', help='External field', type=float, default=0)
    parser.add_argument('-n', '--nstep', type=int, help='Number of datas measured from lattice evolution in a single temperature value', default=100)
    parser.add_argument('-s', '--seed', help='Simulation seed', type = int)
    parser.add_argument('-file', '--out_file', help='Output .txt filename with observable(s) datas. If nothing given, a standard filename will be assigned. If no observable given, will be ignored', default='')
    parser.add_argument('-p', '--path', help="Output file directory path. If 'n' given, datas will not be saved. If no observable given, will be ignored", default = os.curdir)
    parser.add_argument('-no_save', '--save_storie', action='store_false', help='Command to not save MonteCarlo stories. Default True', default=True)
    parser.add_argument('-load', help='Load simulation parameters from file. File must be formatted as key = value (with newlines between different keys) using as keys the --args.')
    opts = parser.parse_args(args)
    
    if not args:
        parser.print_help()
        return options
    
    if opts.load:
        opts = file_opts(opts, opt_keys)
        


    for keys in opt_keys[2:]:
        options[keys] = getattr(opts, keys, None)
    

    #Set some mode-dependent default values
    options['take_storie'] = True
    options['rngstatus'] = None


    if opts.i:
        return user_query(options, supp_opts=supp_opts)


    #No mode 2 allowed if the program is not in interactive mode
    options['mod'] = True

    #L and beta are required
    if not (options['L'] and options['beta_lower']):
        raise errors.OptionError('L and beta_lower required to start a simulation')

    #Setup for getting all the observables
    if 'all' in options['oss'] :
        options['oss'] = supp_opts

    if options['L'] <= 0:
        raise errors.OptionError('L\nLattice dimension must be a positive integer')

    if options['beta_lower'] <= 0:
        raise errors.OptionError('lower temperature\nThe temperature must be a positive float')
    

    #Correcting eventual unused grain option
    if options['beta_upper'] is None:
        options['beta_upper'] = options['beta_lower']
        if options['grain']:
            print('No upper temperature selected, temperature step -gr ' + str(options['grain']) + ' will be ignored')
            options['grain'] = None
    
    
    if options['beta_upper'] <= 0:
        raise errors.OptionError('upper temperature\nThe temperature must be a positive float')

    if options['beta_upper'] < options['beta_lower']:
        raise errors.OptionError('upper temperatur\nUpper temperature option must be lower than lower temperature option')

    options['unitx'] = options['unitx'].lower() =='y' and 'T' or 'beta'

    #Adjusting grain value
    if  options['grain'] is not None:
        if options['grain'] <= 0:
            raise errors.OptionError('Step along temperature axis\nStep along temperature axis must be a positive float')

        elif options['unitx'] == 'beta' and options['grain'] < 0.0001 :
            raise errors.OptionError('Step along temperature axis\nStep along temperature axis too small (minimum = 0.0001)')

        elif options['unitx'] == 'T' and options['grain'] < 0.001 :
            raise errors.OptionError('Step along temperature axis\nStep along temperature axis too small (minimum = 0.001)')
    else:
        options['grain'] = options['unitx'] == 'T' and 0.2 or 0.01
    

    #Checking if seed and number of steps are positive
    if options['nstep'] <=0:
        raise errors.OptionError('number of steps\nNumber of MonteCarlo iterations must be a positive integer')

    if options['seed'] and (options['seed'] <0):
        raise errors.OptionError('seed\nSeed must be a positive integer')
    
    #Removing .txt from parsed argument if present
    if options['out_file']:
        options['out_file'] = options['out_file'].split('.txt')[0]

    #print(options)
    return user_save(options)







def user_query(def_opts: ising_type.tpopt, supp_opts: tp.List[str]) -> ising_type.tpopt:
    '''Set options in interactive mode'''
    #copying default options generated from argparse
    opts = def_opts.copy()

    #welcome string
    print('{:#^61}\n\n{}'.format('  classical ising 2D simulation project  '.title(), 'Choose program mode:'))

    #user choice between mode
    while True:
        temp = input('1: simulation\t\t\t2: plot the previous results\n').lower().strip()
        if temp in ['1','','2'] :
            break
        elif temp == 'q':
            print('Quitting')
            sys.exit(0)
        else:
            print('Not understood, try again. Press q to quit')

    opts['mod'] = (temp in ['1',''])

    #Case 2: plot previous results
    if not opts['mod']:
        opts['out_file'] = input('You are currently in:\n{}\nInsert file path/filename or filename if it is in the cwd \n'.format(os.getcwd())).strip()

    #Case 1: simulation
    else:
        temp = input('Insert lattice (LxL) dimension \nL = ')
        try:
            opts['L'] = int(temp)
            if opts['L'] <= 0:
                raise errors.OptionError('L\nL must be a positive integer')
        except ValueError:
            raise errors.OptionError('L\nL must be a positive integer')
            
        #extfield
        msg = 'Insert external field strength [default: {:.3f}]:\nh = '
        temp = input(msg.format(opts['extfield']))
        if temp:
            try:
                opts['extfield'] = float(temp)
            except ValueError:
                raise errors.OptionError('External field strength\nExternal field strength must be a float')

        #observables
        temp = input('Insert observable(s) between: all, ' + ', '.join(supp_opts) + '\nIf nothing given, only MonteCarlo stories will be generated\n').lower().replace(',',' ')
        res = set( temp.split() )
        if res:
            if 'all' in res:
                res = supp_opts
            elif not( ( res <= set(supp_opts) )):
                raise errors.OptionError('observable(s)\nObservable(s) must be at least one between [all, '+ ', '.join(supp_opts)+']')
            opts['oss'] = list( res )

        #temperature
        while True:
            temp = input('Default temperature unit: beta=1/T. Change into T? (Y/N) [default: N]\n').lower().strip()
            if temp in ['y','','n'] :
                break
            else:
                print('Not understood, try again.')
        opts['unitx'] , opts['grain'] = (temp in ['n','']) and ('beta', 0.01) or ('T', 0.2)
        temp = input('Insert lower temperature:\n' + opts['unitx'] + ' lower = ')
        try:
            opts['beta_lower'] = float(temp)
            if opts['beta_lower'] <= 0:
                raise errors.OptionError('lower temperature\nThe temperature must be a positive float')
        except ValueError:
            raise errors.OptionError('lower temperature\nThe temperature must be a positive float')
        temp = input('Insert upper temperature:\n' + opts['unitx'] + ' upper = ')
        try:
            opts['beta_upper'] = float(temp)
            if opts['beta_upper'] <= 0:
                raise errors.OptionError('upper temperature\nThe temperature must be a positive float')
        except ValueError:
            raise errors.OptionError('upper temperature\nThe temperature must be a positive float')

        #Correcting eventual exchange of upper and lower temperatures
        if opts['beta_lower'] > opts['beta_upper']:
            print('Lower and upper temperatures inverted.  Correcting.')
            opts['beta_lower'], opts['beta_upper'] = opts['beta_upper'], opts['beta_lower']

        #asks for a grain only if a range of beta is requested
        if opts['beta_lower'] != opts['beta_upper']:
            msg = 'Step along temperature axis. Minimum ' + (opts['unitx'] == 'T' and ('0.001' + ' [default: {:.1f}]:\n') or ('0.0001' + ' [default: {:.2f}]:\n')) + opts['unitx']+' grain = '
            temp = input(msg.format(opts['grain']))
            if temp:
                try:
                    opts['grain'] = float(temp)
                    if opts['grain'] <= 0:
                        raise errors.OptionError('Step along temperature axis\nStep along temperature axis must be a positive float')
                    elif opts['unitx'] == 'beta' and opts['grain'] < 0.0001 :
                        raise errors.OptionError('Step along temperature axis\nStep along temperature axis too small')
                    elif opts['unitx'] == 'T' and opts['grain'] < 0.001 :
                        raise errors.OptionError('Step along temperature axis\nStep along temperature axis too small')
                except ValueError:
                    raise errors.OptionError('Step along temperature axis\nStep along temperature axis must be a positive float')
       
       #MonteCarlo iterations     
        temp = input(f"Insert number of MonteCarlo steps (1 iter -> 1 lattice update): [default: {opts['nstep']}]\nnstep = ")
        if temp:
            try:
                opts['nstep'] = int(temp)
                if opts['nstep'] <= 0:
                    raise errors.OptionError('number of step MonteCarlo steps\nNumber of Step MonteCarlo steps must be a positive integer')
            except ValueError:
                 raise errors.OptionError('number of step MonteCarlo steps\nNumber of Step MonteCarlo steps must be a positive integer')
        
        #Seed
        temp = input(f"Insert random number generator seed: [default: {opts['seed']}]\nseed = ")
        if temp:
            try:
                opts['seed'] = int(temp)
                if opts['seed'] <= 0:
                    raise errors.OptionError('seed\nSeed must be a positive integer')
            except ValueError:
                 raise errors.OptionError('seed\nSeed must be a positive integer')
        
        #Calls function to set saving options
        user_save(opts, True)
    return opts




def file_opts(opts: tp.Type[argparse.ArgumentParser], opt_keys: tp.List[str]) -> tp.Type[argparse.ArgumentParser]:
    '''Function to read options from file opts.load'''
    #Sublists of options with different types
    int_arg = ['L','seed','nstep']
    float_arg = ['beta_lower', 'beta_upper', 'grain', 'extfield']
    bool_arg = ['save_storie']

    file1 = open(opts.load, 'r')
    for line in file1:
        if line != '\n':
            temp = line.split('=')

            if temp[0].strip() == 'i':
                raise errors.LoadError('Interactive mode not available from file')

            if len(temp) != 2 and temp[0].strip() !='no_save':
                raise errors.LoadError( f'Line {temp} has wrong format.\nArguments in file must be formatted as key = value')
            
            temp[0] = temp[0].strip() 
            if temp[0] in opt_keys:
                #set attributes in opts, with the correct typing
                if temp[0] in int_arg:
                    setattr(opts, temp[0], int(temp[1]))
                elif temp[0] in float_arg:
                    setattr(opts, temp[0], float(temp[1]))
                elif temp[0] in bool_arg:
                    setattr(opts, temp[0], bool(temp[1].strip()))
                elif temp[0] == 'oss':
                    setattr(opts, temp[0], temp[1].lower().replace(',',' ').split())
                else:
                    setattr(opts, temp[0], temp[1].strip())
    file1.close()
    return opts




def user_save(opts: ising_type.tpopt, user: bool = False) -> ising_type.tpopt:
    '''Set saving options: path and filename of resulting observable calculation and MonteCarlo stories'''
    #If there is any observable to calculate, asks if and where to save the results. Otherwise save only MonteCarlo stories
    if not opts['oss']:

        opts['path'] = None
        opts['out_file'] = None
        opts['save_storie'] = True
    
    else:
        if user:
            save = input('Save the results? If yes, insert directory path [default: {}]. If no, insert N\n'.format(os.getcwd())).strip()
            opts['path'] = save == '' and os.curdir or save

        #If no save required
        if opts['path'].lower()=='n':
            opts['path']=None
            opts['out_file'] = None

        #Setting saving options
        else:
            flag = True
            while flag:
                if os.path.exists(opts['path']):
                    flag=False
                else:
                    flag2 = True
                    while flag2:
                        #Check if the directory exists
                        i = input(f"{opts['path']} directory does not exist. Create? (Y/N)\n" ).lower().strip()
                        if i == 'y':
                            try:
                                os.mkdir(opts['path'])
                                flag2 = False
                                flag = False
                            except FileNotFoundError:
                                raise errors.OptionError('path\nWrong input path %s'%opts['path'])
                        elif i == 'n':
                            flag2=False
                            save = input('Insert path [default: {}]\n'.format(os.getcwd())).strip()
                            opts['path'] = save == '' and os.curdir or save
                        else:
                            print('Not understood, try again.')

            flag = True
            #Setting output filename 
            default_name = "{}_L{a[L]}_h{a[extfield]:.3f}".format('_'.join(opts['oss']),a = opts)
            fmt = 'Insert output file (txt) name [default: {}]\n'.format( default_name )
            user2 = user
            while flag:
                if user2:
                    opts['out_file'] = input(fmt).strip().split('.txt')[0]

                if not opts['out_file']:
                    fmt = 'Insert output file (txt) name [default already exists]\n'

                opts['out_file'] = opts['out_file'] == '' and default_name or opts['out_file']
                if os.path.exists(opts['path']+os.sep+opts['out_file']+os.extsep+'txt'):
                    flag2 =True
                    while flag2:
                        i=input('{} does already exist. Overwrite? (Y/N)\n'.format(opts['out_file']+os.extsep+'txt')).lower().strip()
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

            #Assigning filename with extension .txt
            opts['out_file'] = opts['out_file'] + os.extsep + 'txt'

        #Asking the user whether to save or not MonteCarlo stories
        if user:
            msg1 = '''Save (into the directory ''{}L={}'') MonteCarlo stories to enhance future simulations? (Y/N) [default: Y]\n'''.format(os.curdir+os.sep+'MC_stories'+os.sep , opts['L'])
            opts['save_storie'] = sml.user_while(msg1, df = 'y' )
            
    #Saving MonteCarlo stories, checking if the directory exists, creating it otherwise
    if opts['save_storie']:
        if 'MC_stories' not in os.listdir(os.curdir):
            os.mkdir('MC_stories')
            print('Directory MC_stories created')
        if f"L={opts['L']}" not in os.listdir(os.curdir + os.sep + 'MC_stories'):
            opts['take_storie'] = False
            os.mkdir(os.curdir+os.sep+'MC_stories'+os.sep+f"L={opts['L']}" )
            print(f"Directory L={opts['L']} created" )
        if  not (user and opts['oss']):
            print('MonteCarlo stories will be saved into the directory ''{}L={}'''.format(os.curdir+os.sep+'MC_stories'+os.sep , opts['L']))  

    return opts



