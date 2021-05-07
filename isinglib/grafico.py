import numpy as np
import time
import matplotlib.pyplot as plt
from isinglib import classe_reticolo as ret
from isinglib import bootstrap as bts


def grafico_completo(obj_reticolo, beta, nstep, nspazzate,  nome):
    #da riguardare
    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))

    for i in beta:
        obj_reticolo.gen_exp(i)
        A = bts.simulazione(obj_reticolo, nstep = nstep, nspazzate = nspazzate, nome = nome)
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
        ax.imshow(obj_reticolo.mat, cmap='tab20c_r')
        figure.canvas.draw()
        figure.canvas.flush_events()
        time.sleep(0.1)




def grafico_old(L, beta_v, nstep, nspazzate, nome='|m|'):
    #da riguardare
    y=[]
    dy=[]
    for i in beta_v:
        A = bts.punto(L, i, nstep=nstep, nspazzate=nspazzate, nome=nome)
        y.append(A['valore'])
        dy.append(A['errore'])

    plt.errorbar(beta_v, y, dy)
    plt.xlabel('Beta')
    plt.ylabel(nome)
    plt.grid()
    plt.show()

def asse_y(L, asse_x, nstep, nspazzate, nome='amag', unit_x='BETA'):
    '''prende in input l'asse x della temperatura in unità unit_x = 'T' (oppure 'BETA') e restituisce in output l'asse y con incertezza dy della quantità "nome"'''
    #da controllare per bene
    quant = nome in ['amag','chi','mag','binder'] and 1 or -1
    materia_prima = quant == 1 and 'magn' or 'ene'
    y=[]
    dy=[]
    f = (unit_x == 'T') and (lambda x: 1/x) or (lambda x: x)
    obj_reticolo=ret.Reticolo(L, f(asse_x[0]), seed=10)
    for i in asse_x:
        obj_reticolo.gen_exp(f(i), b_term=True)
        v=bts.step(obj_reticolo, nstep=nstep, nspazzate=nspazzate, nome = quant)[materia_prima]
        A = bts.punto(v, L, nome=nome)
        v.clear() #se lo tolgo va male.. non capisco bene perchè.. alla fine ridefinisco v boh! E' come se facessi v+=bts.step(....) . Davide, che ne pensi?
        y.append(A['valore'])
        dy.append(A['errore'])
    return y, dy
    
def plot_grafico(L, asse_x, nstep, nspazzate, nome='amag', unit_x='BETA'):
    '''prende in input l'asse x della temperatura in unità unit_x = 'T' (oppure 'BETA') e restituisce in output l'asse y con incertezza dy della quantità "nome"'''
    y, dy = asse_y(L, asse_x, nstep, nspazzate, nome, unit_x)
    plt.errorbar(asse_x, y, dy)
    plt.xlabel(unit_x)
    plt.ylabel(nome)
    plt.grid()
    plt.show()
