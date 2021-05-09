import numpy as np
import time
import matplotlib.pyplot as plt
from isinglib import classe_reticolo as ret
from isinglib import bootstrap as bts
from isinglib import salva
import os

def asse_y(L, asse_x, nstep, nspazzate, h=0, nome='amag', unit_x='beta'):#da mettere nel main (pensiamoci)
    '''prende in input l'asse x della temperatura in unità unit_x = 'T' (oppure 'beta') e restituisce in output l'asse y con incertezza dy della quantità "nome"'''
    quant , materia_prima = nome in ['amag','chi','mag','binder'] and (1,'magn') or (-1,'ene')
    os.makedirs('L={}'.format(L),exist_ok=True)
    os.chdir('L={}'.format(L))
    y=[]
    dy=[]
    f = (unit_x == 'T') and (lambda x: 1/x) or (lambda x: x)
    obj_reticolo = ret.Reticolo(L, f(asse_x[0]), term=0, extfield = h, seed=np.random.randint(10000))#davide, poi ricordiamoci di aggiustare il seed
    for i in asse_x:
        v={ 'ene': [] , 'magn': [] }
        fmt = 'h{h:.2f}_beta{beta:.3f}'.format(beta=f(i),h=h).replace('.',',')+os.extsep+'txt'
        if fmt in os.listdir(os.curdir):
            file_data = open(fmt, 'r')
            opts=salva.reticolo_storia(file_data)
            v=opts['vec']
            file_data.close()
            obj_reticolo.gen_exp(f(i), h)#davide, poi qua discutiamo se ha senso mettere il seed
            obj_reticolo.inizializza(L, term=0, conf_in=opts['reticolo'])
        else:
            obj_reticolo.gen_exp(f(i), h, b_term=True)#forse metti fuori
        v[materia_prima].extend(bts.step(obj_reticolo, nstep=nstep, nspazzate=nspazzate, nome = quant)[materia_prima])
        A = bts.punto(v[materia_prima], L, nome=nome)
        file_data = open(fmt, 'w')
        salva.salva_storia(obj_reticolo, nspazzate, v, file_data)
        file_data.close()
        y.append(A['valore'])
        dy.append(A['errore'])
    return y, dy
    
def plot_grafico(x, y, dy, L , h=0, nome_x='beta', nome_y='chi', salva_file=False, plot=True):#controllare! mettere unita nel file di testo
    '''prende in input l'asse x, l'asse y e l'incertezza su y della temperatura in unità unit_x = 'T' (oppure 'beta') e restituisce in output l'asse y con incertezza dy della quantità "nome".
    Se salva_file=True, salva su file i dati del grafico.
    Se plot=True, stampa il plot.
    '''
    
    if salva_file:
        fmt='{}_h{h:.2f}_L{L}{ext}'.format(nome_y,h=h,L=L,ext=os.extsep+'txt')#modifica Fra
        file_data = open(fmt, 'w')
        print('Grafico di '+nome_y,file=file_data)
        print('L=%d, h=%.2f'%(L,h),file=file_data)
        for x1, y1, dy1 in zip(x, y, dy):
            print('%.3f %.5f %.5f'%(x1,y1,dy1),file=file_data)
        file_data.close()
    if plot:
        plt.errorbar(x, y, dy,  marker = '.')
        plt.title( 'L=%d, h=%.2f'%(L,h) )
        plt.xlabel(nome_x)
        plt.ylabel(nome_y)
        plt.grid()
        plt.show()


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

