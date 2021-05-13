'''Programma principale per la generazione di dati sul modello di Ising'''

from isinglib import classe_reticolo as ret
from isinglib import bootstrap as bts
from isinglib import grafico as grf
from isinglib import errors
from isinglib import salva
from isinglib import user
import numpy as np
import sys
import os





supp_obs = ['binder','chi','amag','mag','c','ene']
usage_msg='2D ising model simulator'

try:
    opts = user.set_options(sys.argv[0], sys.argv[1:], supp_obs, usage_msg=usage_msg)
    if not opts:
        print('No argument given, closing')
        sys.exit(0)
except errors.OptionError as e:
    print('Error found while parsing option')
    print(e)
    sys.exit(1)

if not opts['mod']:
    try:
        grf.mode_2(opts['out_file'])
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

else:
    x_axis=[opts['beta_lower'] + i*opts['grain'] for i in range(1 + int(np.rint((opts['beta_upper'] - opts['beta_lower'])/opts['grain'])))]
    d_oss = { oss : {'valore': [], 'errore': []} for oss in opts['oss'] }
    #f , x_name = (opts['unitx'] == 'y') and ((lambda x: 1/x), 'T')  or ((lambda x: x) , 'beta')
    f = (opts['unitx'] == 'T') and (lambda x: 1/x)  or (lambda x: x)


    if 'L={}'.format(opts['L']) not in os.listdir(os.curdir+os.sep+'MC_stories'):
        opts['take_storie'] = False
    else:
        os.chdir(os.curdir+os.sep+'MC_stories' + os.sep + 'L={}'.format(opts['L']))
    flag=True

    obj_reticolo = ret.Reticolo(opts['L'], f(x_axis[0]), term=0, extfield = opts['extfield'], seed=opts['seed'])
    rng_status = obj_reticolo.rng.bit_generator.state

    for x in x_axis:
        v = { 'ene' : [] , 'magn' : [] }
        flag5 = False
        fmt = {'beta':'h{h:.3f}_beta{beta:.4f}'.format(h=opts['extfield'],beta=f(x)).replace('.',',')+os.extsep+'txt', 'T': 'h{h:.3f}_T{beta:.3f}'.format(h=opts['extfield'],beta=1/f(x)).replace('.',',')+os.extsep+'txt'}
        if flag and opts['take_storie'] and (fmt[opts['unitx']] in os.listdir(os.curdir)):
            flag = False
            fmt2 = opts['save_storie'] and '\nWARNING: if N, the previous matching stories will be overwritten\n' or '\n'
            fmt2 = ('Found MonteCarlo stories in the directory L={} with L, extfield and temperatures matching your previous inputs. Use them to improve the current simulation? (Y/N) [default: Y]\nIf Y, file seeds will be used.' + fmt2).format(opts['L'])
            opts['take_storie'] = user.user_while(fmt2)
            
        if opts['take_storie'] and (fmt[opts['unitx']] in os.listdir(os.curdir)):#importante ordine
            file_data = open(fmt[opts['unitx']], 'r')
            try:
                dataf = salva.reticolo_storia(file_data)
            except errors.LoadError as e:
                print('Error found while reading datas from '+os.path.abspath(os.curdir)+os.sep+fmt[opts['unitx']])
                print(e)
                sys.exit(1)
            v = dataf['vec']
            file_data.close()
            try:
                obj_reticolo = ret.Reticolo(opts['L'], f(x), term=0, extfield = opts['extfield'], conf_in = dataf['mat'], seed = dataf['seed'], state = dataf['rngstatus'])
            except errors.InitializationError as e:
                print('Error found while reading datas from '+os.path.abspath(os.curdir)+os.sep+fmt[opts['unitx']])
                print(e)
                sys.exit(1)
        else:
            obj_reticolo.seed = opts['seed']
            obj_reticolo.rng.bit_generator.state = rng_status
            obj_reticolo.gen_exp(f(x), extfield = opts['extfield'] )
            obj_reticolo.update_metropolis(opts['L']**2)
            flag5 = True
            
        #controllo se calcolare energia o magn o entrambe
        
        quant = 0
        if set(opts['oss']) & {'amag','chi','mag','binder'} :
            quant = 1
        if set(opts['oss']) & {'c','ene'} :
            quant -=1

        matter = bts.step(obj_reticolo, nstep = opts['nstep'], nome = quant)
        if flag5:
            rng_status = obj_reticolo.rng.bit_generator.state
        
        v['ene'].extend(matter['ene'])
        v['magn'].extend(matter['magn'])

        if opts['save_storie']:
            file_data = open(fmt[opts['unitx']], 'w')
            salva.salva_storia(obj_reticolo, vec=v, file_data=file_data)
            file_data.close()

        for oss in opts['oss']:
            P = bts.punto(v[bts.find_matter(oss)], opts['L'], nome = oss)
            d_oss[oss]['valore'].append(P['valore'])
            d_oss[oss]['errore'].append(P['errore'])
            
    if (opts['take_storie'] or opts['save_storie']):#chiedi
        os.chdir(os.pardir+os.sep+os.pardir)
    if opts['path']:
        salva.func_save(opts['L'], opts['extfield'], opts['unitx'], x_axis, d_oss, opts['out_file'], opts['path'])

    if len(x_axis)==1:
        for oss in opts['oss']:
            if d_oss[oss]['errore'][0] >=1:
                fmt_res = '{} = {} +\- {}'.format(oss, int(np.rint(d_oss[oss]['valore'][0])), int(np.rint(d_oss[oss]['errore'][0])))
            else:
                s = str(d_oss[oss]['errore'][0]).split('.')[1]
                i=1 + len(s) - len(s.lstrip('0'))
                fmt_res = ('{} = {:.'+ str(i) +'f} +\- {:.'+str(i)+'f}').format(oss, d_oss[oss]['valore'][0], d_oss[oss]['errore'][0])
            print(fmt_res)
    else:
        for oss in opts['oss']:
            grf.plot_graph(x_axis, d_oss[oss]['valore'], d_oss[oss]['errore'], opts['L'] ,opts['extfield'], opts['unitx'], oss)


    




