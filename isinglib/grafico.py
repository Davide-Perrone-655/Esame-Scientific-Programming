import numpy as np
import matplotlib.pyplot as plt
from isinglib import bootstrap as bts

def grafico_mag(L, beta_v, nstep, nspazzate, bin=1):
    y=[]
    dy=[]
    for i in beta_v:
        A = bts.punto(L, i, nstep=nstep, nspazzate=nspazzate, bin=bin, nome='|m|')
        y.append(A['valore'])
        dy.append(A['errore'])

    plt.errorbar(beta_v, y, dy)
    plt.xlabel('Beta')
    plt.ylabel('Magnetizzazione')
    plt.grid()
    plt.show()

def grafico_chi(L, beta_v, nstep, nspazzate, bin=1):
    y=[]
    dy=[]
    for i in beta_v:
        A = bts.punto(L, i, nstep=nstep, nspazzate=nspazzate, bin=bin, nome='chi')
        y.append(A['valore'])
        dy.append(A['errore'])

    plt.errorbar(beta_v, y, dy)
    plt.xlabel('Beta')
    plt.ylabel('Suscettività')
    plt.grid()
    plt.show()
