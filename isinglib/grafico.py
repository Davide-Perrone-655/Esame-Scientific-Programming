import numpy as np
import time
import matplotlib.pyplot as plt
from isinglib import bootstrap as bts


def grafico_completo(obj_reticolo, beta, nstep, nspazzate, bin_vec, nome):
    #da riguardare
    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))

    for i in beta:
        obj_reticolo.gen_exp(i)
        A = bts.simulazione(obj_reticolo, nstep = nstep, nspazzate = nspazzate, bin_vec = bin_vec, nome = nome)
        y.append(A['valore'])
        dy.append(A['errore'])
        ax.matshow(obj_reticolo.mat)
        figure.canvas.draw()
        figure.canvas.flush_events()
        time.sleep(0.1)
    plt.errorbar(beta, y, dy)
    plt.xlabel('Beta')
    plt.ylabel('Mag')
    plt.grid()
    plt.show()




def grafico_live(obj_reticolo, beta, nstep, nspazzate):
    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    for i in beta:
        obj_reticolo.gen_exp(i)
        for _ in range(nstep):
            obj_reticolo.aggiorna(nspazzate)
        ax.matshow(obj_reticolo.mat)
        figure.canvas.draw()
        figure.canvas.flush_events()
        time.sleep(0.1)




def grafico(L, beta_v, nstep, nspazzate, bin=1, nome='|m|'):
    #da riguardare
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
