import numpy as np
import matplotlib.pyplot as plt
from isinglib import bootstrap as bts

def grafico(L, beta_v, nstep, nspazzate, bin=1, nome='|m|'):
    y=[]
    dy=[]
    for i in beta_v:
        A = bts.punto(L, i, nstep=nstep, nspazzate=nspazzate, bin=bin, nome=nome)
        y.append(A['valore'])
        dy.append(A['errore'])

    plt.errorbar(beta_v, y, dy)
    plt.xlabel('Beta')
    plt.ylabel(nome)
    plt.grid()
    plt.show()
