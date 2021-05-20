#!/usr/bin/env python3

'''2D ising model, main program
Calculates mag (magnetizzation), amag (absolute magnetization value), chi (magnetic susceptibility), e (energy), c (specific heat) and binder (binder cumulant)
from a simulation, using Metropolis algotithm
'''

from isinglib import ising_bootstrap as bts
from isinglib import ising_errors as errors
from isinglib import ising_files as salva
from isinglib import ising_lattice as ret
from isinglib import ising_small as sml
from isinglib import ising_user as user
from isinglib import ising_plot as grf
import numpy as np
import sys
import os


#Check if the user has the correct python version
version = sys.version_info.major >= 3 and sys.version_info.minor >= 6
if not version:
    print('Python 3.6 or later version is needed.')
    sys.exit(3)

#List of supported observables:
supp_obs = ['binder','chi','amag','mag','c','ene']
usage_msg = __doc__

try:
    opts = user.set_options(sys.argv[0], sys.argv[1:], supp_obs, usage_msg = usage_msg)
    if not opts:
        print('No argument given, closing')
        sys.exit(0)
except errors.OptionError as e:
    print('Error found while parsing option')
    print(e)
    sys.exit(1)


#Enter in second mode, plot only a previous simulation
if not opts['mod']:
    #grf.mode_3() trying mode_3
    try:
        grf.mode_2(opts['out_file'])
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    #Raise if there is unexpected or missing information
    except (IndexError, ValueError):
        print(f"File {opts['out_file']} does not match standard results files format")
        sys.exit(2)

#Simulation mode
else:
    #Creates list of beta with given grain and observables dictionary
    x_axis=[opts['beta_lower'] + i*opts['grain'] for i in range(1 + int(np.rint((opts['beta_upper'] - opts['beta_lower'])/opts['grain'])))]
    d_oss = { oss : {'valore': [], 'errore': []} for oss in opts['oss'] }

    #Handles T or beta conversion
    f = (opts['unitx'] == 'T') and (lambda x: 1/x)  or (lambda x: x)

    #Search in library if previous MC stories are present or not
    if f"L={opts['L']}" not in os.listdir(os.curdir+os.sep+'MC_stories'):
        opts['take_storie'] = False
    else:
        os.chdir(os.curdir + os.sep + 'MC_stories' + os.sep + f"L={opts['L']}")
    

    #Initialize lattice with given options and sets rng status
    obj_reticolo = ret.Reticolo(opts['L'], f(x_axis[0]), term=0, extfield = opts['extfield'], seed=opts['seed'])
    rng_status = obj_reticolo.rng.bit_generator.state

    flag=True 

    #Calculates values corresponding to given beta (or T) range
    for x in x_axis:
        v = { 'ene' : [] , 'magn' : [] }
        flag5 = False #Set or restart rng state

        #Dictionary of saved stories names, keys: T, beta; values: filenames
        fmt = {'beta':'h{h:.3f}_beta{beta:.4f}'.format(h=opts['extfield'],beta=f(x)).replace('.',',')+os.extsep+'txt', 'T': 'h{h:.3f}_T{beta:.3f}'.format(h=opts['extfield'],beta=1/f(x)).replace('.',',')+os.extsep+'txt'}
        
        #Asks whether the user wants to use previous simulations to refine current simulation results
        if flag and opts['take_storie'] and (fmt[opts['unitx']] in os.listdir(os.curdir)):

            flag = False #enters here only once

            fmt2 = opts['save_storie'] and '\nWARNING: if N, the previous matching stories will be overwritten\n' or '\n'
            fmt2 = (f"Found MonteCarlo stories in the directory L={opts['L']} with L, extfield and temperatures matching your previous inputs. Use them to improve the current simulation? (Y/N) [default: Y]\nIf Y, file seeds will be used." + fmt2)
            
            #Asks until Y/N
            opts['take_storie'] = sml.user_while(fmt2, df = 'y')
        
        #If the user answered yes: open and read datas
        if opts['take_storie'] and (fmt[opts['unitx']] in os.listdir(os.curdir)):
            file_data = open(fmt[opts['unitx']], 'r')
            try:
                dataf = salva.reticolo_storia(file_data)
            except errors.LoadError as e:
                print('Error found while reading datas from ' + os.getcwd() + os.sep + fmt[opts['unitx']])
                print(e)
                sys.exit(1)
            v = dataf['vec']
            file_data.close()

            #Loads last lattice state and continues the simulation from there
            try:
                obj_reticolo = ret.Reticolo(opts['L'], f(x), term = 0, extfield = opts['extfield'], conf_in = dataf['mat'], seed = dataf['seed'], state = dataf['rngstatus'])
                #A new object is created because it is already at thermal equilibrium
            except errors.InitializationError as e:
                print('Error found while reading datas from ' + os.getcwd() + os.sep + fmt[opts['unitx']])
                print(e)
                sys.exit(1)

        #If the user answered no: creates a new simulation. 
        else:
            obj_reticolo.seed = opts['seed']
            obj_reticolo.rng.bit_generator.state = rng_status 
            obj_reticolo.gen_exp(f(x), extfield = opts['extfield'] )
            obj_reticolo.update_metropolis(opts['L']**2)
            flag5 = True
        #no new object is created because the previous one (at the previous value of temperature) is almost termalized at the current value of temperature (x)

        #Check which observable is needed (both if no observable given, just to save them)
        quant = 0
        if set(opts['oss']) & {'amag','chi','mag','binder'} :
            quant = 1
        if set(opts['oss']) & {'c','ene'} :
            quant -=1

        #Makes steps to calculate observables
        matter = bts.step(obj_reticolo, nstep = opts['nstep'], quant = quant)

        #Setting status (done in order to skip status taken from file)
        if flag5:
            rng_status = obj_reticolo.rng.bit_generator.state
        
        #Extending loaded vector (If none present, extend is the identity operator)
        v['ene'].extend(matter['ene'])
        v['magn'].extend(matter['magn'])

        if opts['save_storie']:
            salva.salva_storia(obj_reticolo, vec = v, file_name = fmt[opts['unitx']])

        #Calculates value and error at the end of the simulation for every requested observable
        for oss in opts['oss']:
            P = bts.punto(v[sml.find_matter(oss)], opts['L'], name = oss)
            d_oss[oss]['valore'].append(P['valore'])
            d_oss[oss]['errore'].append(P['errore'])
        
    #After the for cycle, if there is any story taken or saved (so the program is in the MC_stories/L=/ directory) 
    # returns in the original directory
    if (opts['take_storie'] or opts['save_storie']):
        os.chdir(os.pardir+os.sep+os.pardir)

    #If a path was given (or default given), result file is saved
    if opts['path']:
        salva.func_save(opts['L'], opts['extfield'], opts['unitx'], x_axis, d_oss, opts['out_file'], opts['path'])

    #If the user asked for only one value of beta (or T), prints the results on stdout, otherwise a plot is generated
    if len(x_axis)==1:
        for oss in opts['oss']:

            #Printing with the correct number of significant digits
            if d_oss[oss]['errore'][0] >=1:
                fmt_res = '{} = {} +\- {}'.format(oss, int(np.rint(d_oss[oss]['valore'][0])), int(np.rint(d_oss[oss]['errore'][0])))
            else:
                s = str(d_oss[oss]['errore'][0]).split('.')[1]
                i=1 + len(s) - len(s.lstrip('0'))
                fmt_res = ('{0} = {a[valore][0]:.'+ str(i) +'f} +\- {a[errore][0]:.'+str(i)+'f}').format(oss, a = d_oss[oss])
            print(fmt_res)

    #Plots a graph for every observable
    else:
        for oss in opts['oss']:
            #blocking last plot
            block = oss == opts['oss'][-1]
            grf.plot_graph(x_axis, d_oss[oss]['valore'], d_oss[oss]['errore'], opts['L'] ,opts['extfield'], opts['unitx'], oss, block_fig = block)


    




