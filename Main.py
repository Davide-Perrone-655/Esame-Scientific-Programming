"""
Programma principale per la generazione di dati sul modello di Ising
"""

import numpy as np
import matplotlib.pyplot as plt
from isinglib import bootstrap as bts
from isinglib import grafico as grf
from isinglib import classe_reticolo as ret
#from isinglib import bootstrap

beta=np.linspace(0.30, 0.55, 20)
#print(beta)
L = 10
nstep = 100
nspazzate = 1
bin_vec = 10
y=[]
dy=[]
lattice = ret.Reticolo(L, beta[0], seed=10)
print(lattice.mat)

for i in beta:
    lattice.gen_exp(i)
    A = bts.simulazione(lattice, nstep = nstep, nspazzate = nspazzate, bin_vec = bin_vec, nome = 'chi')
    y.append(A['valore'])
    dy.append(A['errore'])

plt.errorbar(beta, y, dy)
plt.xlabel('Beta')
plt.ylabel('Mag')
plt.grid()
plt.show()

#print(magn['valore'],'+-', magn['errore'])



