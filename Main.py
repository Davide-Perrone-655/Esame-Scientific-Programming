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
import os


options = user.default_options()
options = user.user_query(options)

print(options.keys())
print(options)
lattice = ret.Reticolo(options['L'], options['beta'], extfield=options['extfield'])
print(lattice.mat)








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




