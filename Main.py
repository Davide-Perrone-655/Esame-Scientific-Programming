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

#beta=np.linspace(0.30, 0.55, 2)
path = '.'
filename = 'data.dat'
beta=0.3
print(beta)
L = 25
nstep = 100
nspazzate = 1
bin_vec = 10
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


print('#L=%d' %L, file=file_data)
print('#SEED=%d' %seed, file=file_data)
print('#RNGSTATUS=', file=file_data)
print('#TITLE=%s' %nome, file=file_data)


vec=bts.step(lattice, nstep=nstep, nspazzate=nspazzate, nome=-1)
print(vec)
salva.salva_storia(lattice, vec, file_data)
A=bts.punto(vec['ene'], L, nome='e')
print(A)
file_data.close()
#grf.grafico_live(lattice, beta, nstep, nspazzate)

"""
plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))

for i in beta:
    lattice.gen_exp(i)
    A = bts.simulazione(lattice, nstep = nstep, nspazzate = nspazzate, bin_vec = bin_vec, nome = 'chi')
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

#ciao
#print(magn['valore'],'+-', magn['errore'])



