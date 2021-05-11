"""
Programma principale per la generazione di dati sul modello di Ising
"""
import time
import numpy as np
import matplotlib.pyplot as plt
from isinglib import bootstrap as bts
from isinglib import grafico as grf
from isinglib import classe_reticolo as ret
from isinglib import salva
from isinglib import user
from isinglib import errors
import os
import sys

def find_matter(oss):
    if oss in {'amag','chi','mag','binder'} :
        return 'magn'
    return 'ene'

supp_obs = ('binder','chi','amag','mag','c','ene')
msg='Programma modello di Ising'
   
try:
    opts = user.set_options(sys.argv[0], sys.argv[1:], supp_obs, msg)
    if not opts:
        print('No argument given, closing')
        sys.exit(0)
except errors.OptionError as e:
    print('Error found while parsing option')
    print(e)
    sys.exit(1)
print(opts)
x_axis=[opts['beta_lower'] + i*opts['grain'] for i in range(1 + int((opts['beta_upper'] -opts['beta_lower'])/opts['grain']))]
d_oss = { oss : {'valore': [], 'errore': []} for oss in opts['oss'] }
f , x_name = (opts['unitx'] == 'y') and ((lambda x: 1/x), 'T')  or ((lambda x: x) , 'beta')
if 'L={}'.format(opts['L']) not in os.listdir(os.curdir+os.sep+'MC_stories'):
    opts['take_storie'] = False
else:
    os.chdir(os.curdir+os.sep+'MC_stories' + os.sep + 'L={}'.format(opts['L']))
flag=True

obj_reticolo = ret.Reticolo(opts['L'], f(x_axis[0]), term=0, extfield = opts['extfield'], seed=opts['seed'])#davide, poi ricordiamoci di aggiustare il seed
rng_status = obj_reticolo.rng.bit_generator.state
for x in x_axis:
    v = { 'ene' : [] , 'magn' : [] }
    flag5 = False
    fmt = 'h{h:.2f}_beta{beta:.3f}'.format(h=opts['extfield'],beta=f(x)).replace('.',',')+os.extsep+'txt'
    if flag and opts['take_storie'] and (fmt in os.listdir(os.curdir)):#importante ordine
        flag = False
        while True:
            fmt2 = opts['save_storie'] and '\nWARNING: if N, the previous matching stories will be overwritten\n' or '\n'
            temp = input( ('Found MonteCarlo stories in the directory L={} with L, extfield and temperatures matching your previous inputs. Use them to improve the current simulation? Y/N [default: Y]\nIf Y, file seeds will be used.'+fmt2).format(opts['L']) ).lower().strip()
            if temp in ['y','']:
                opts['take_storie'] = True
                break
            elif temp == 'n':
                opts['take_storie'] = False
                break
            else:
                print('Not understood, try again.')
    if opts['take_storie'] and (fmt in os.listdir(os.curdir)):#importante ordine
        file_data = open(fmt, 'r')
        dataf = salva.reticolo_storia(file_data)
        v = dataf['vec']
        file_data.close()
        obj_reticolo = ret.Reticolo(opts['L'], f(x), term=0, extfield = opts['extfield'], conf_in = dataf['mat'], seed = dataf['seed'], state = dataf['rngstatus'])#va rifatto? oppure settiamo il seed e lo status? A sto punto rifacciamolo
    else:
        obj_reticolo.seed = opts['seed']
        obj_reticolo.rng.bit_generator.state = rng_status
        obj_reticolo.gen_exp(f(x), extfield = opts['extfield'] , b_term=True)#forse metti fuori
        flag5 = True
        
    #controllo se calcolare energia o magn o entrambe
    quant = -1
    if set(opts['oss']) & {'amag','chi','mag','binder'} :
        if set(opts['oss']) & {'c','ene'} :
            quant = 0
        else:
            quant = 1
    matter = bts.step(obj_reticolo, nstep = opts['nstep'], nspazzate = 1, nome = quant)
    if flag5:
        rng_status = obj_reticolo.rng.bit_generator.state
    
    v['ene'].extend(matter['ene'])
    v['magn'].extend(matter['magn'])
    if opts['save_storie']:
        file_data = open(fmt, 'w')
        salva.salva_storia(obj_reticolo, nspazzate=1, vec=v, file_data=file_data)
        file_data.close()
    for oss in opts['oss']:
        P = bts.punto(v[find_matter(oss)], opts['L'], nome = oss)
        d_oss[oss]['valore'].append(P['valore'])
        d_oss[oss]['errore'].append(P['errore'])
if (opts['take_storie'] or opts['save_storie']):#chiedi
    os.chdir(os.pardir+os.sep+os.pardir)
if opts['path']:
    grf.func_save(opts['L'], opts['extfield'], x_name, x_axis, d_oss, opts['out_file'], opts['path'])
for oss in opts['oss']:
    grf.plot_graph(x_axis, d_oss[oss]['valore'], d_oss[oss]['errore'], opts['L'] ,opts['extfield'], x_name, oss)



        

    






"""
path = os.curdir
filename = 'data.txt'
beta = 0.2
L = 3
nstep = 100
nspazzate = 1
extfield = 0
y=[]
dy=[]
nome = 'ene'
seed=10



asse_x = list(np.linspace(0.01,10,100))
y, dy = grf.asse_y(L, asse_x, nstep, nspazzate, h=extfield , unit_x='T', nome='amag')
grf.plot_grafico(asse_x, y, dy, L, h=extfield, nome_x='T', nome_y='amag',salva_file=True,plot=True)

if filename in os.listdir(path):
    print('File già esistente, sovrascrivo')
    file_data = open(filename, 'w')
else:
    file_data = open(filename, 'x')
lattice = ret.Reticolo(L, beta, seed=seed)
vec=bts.step(lattice, nstep=nstep, nspazzate=nspazzate, nome=0)
print(len(vec['magn']))
print(bts.punto(vec['magn'], L, nome='chi'))
salva.salva_storia(lattice, nspazzate, vec, file_data)
file_data.close()
#grf.grafico_live(lattice, beta, nstep, nspazzate)
nstep = 100
file_data=open("data.txt",'r')
opts=salva.reticolo_storia(file_data)
L=opts['L']
beta=opts['beta']
seed=opts['seed']
nspazzate=opts['nspazzate']
conf_in=opts['reticolo']
vec=opts['vec']
print(len(vec['magn']))
print(bts.punto(vec['magn'], L, nome='chi'))
lattice = ret.Reticolo(L, beta, term=0, seed=seed, conf_in = conf_in)#Se diamo il reticolo da File non c'è bisogno della termalizzazione!!
for key in vec.keys():
    vec[key].extend(bts.step(lattice, nstep=nstep, nspazzate=nspazzate, nome = 0 )[key])
print(len(vec['magn']))
print(bts.punto(vec['magn'], L, nome='chi'))
file_data.close()

plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))

for i in beta:
    lattice.gen_exp(i)
    A = bts.simulazione(lattice, nstep = nstep, nspazzate = nspazzate, nome = 'chi')
    y.append(A['valore'])
    dy.append(A['errore'])
    ax.matshow(lattice.mat)
    figure.canvas.draw()
    figure.canvas.flush_events()
    time.sleep(0.1)

plt.errorbar(beta, y, dy)
plt.xlabel('Beta')
plt.ylabel('Mag')
plt.grid()
plt.show()
"""




