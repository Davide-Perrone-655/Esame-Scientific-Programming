"""
Programma principale per la generazione di dati sul modello di Ising
"""

import numpy as np
import matplotlib.pyplot as plt
from isinglib import bootstrap as bts
from isinglib import grafico as grf
#from isinglib import bootstrap

beta=np.linspace(0.30, 0.55, 20)
#print(beta)
L=10
nstep=100
nspazzate=1
bin=1
#magn = bts.punto(L, beta, 0, nstep, nspazzate, bin,'e')
grf.grafico_mag(L, beta, nstep, nspazzate, bin)
grf.grafico_chi(L, beta, nstep, nspazzate, bin)

#print(magn['valore'],'+-', magn['errore'])



