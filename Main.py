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
import os
#from isinglib import bootstrap


path = '.'
filename = 'data.txt'
beta=0.2
print(beta)
L = 10
nstep = 100
nspazzate = 1
extfield=0
y=[]
dy=[]
nome = 'ene'
seed=10

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
#grf.grafico_live(lattice, beta, nstep, nspazzate)"""
nstep = 100
file_data=open("data.txt",'r')
opts=salva.reticolo_storia(file_data)
L=opts['L']
beta=opts['beta']
seed=opts['seed']
nspazzate=opts['nspazzate']
conf_in=opts['reticolo']
nspazzate=opts['nspazzate']
lattice = ret.Reticolo(L, beta, term=0, seed=seed, conf_in = conf_in)#Se diamo il reticolo da File non c'è bisogno della termalizzazione!!
vec=opts['vec']
vec=bts.step(lattice, nstep=nstep, nspazzate=nspazzate, nome = 0 , vec=vec)
print(len(vec['magn']))
print(bts.punto(vec['magn'], L, nome='chi'))
file_data.close()

"""
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




