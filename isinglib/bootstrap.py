import time
import numpy as np
from isinglib import classe_reticolo as ret


rng = np.random.default_rng()


def bootstrap(osservabile, vec, boot_cycle=10):
    bootk=[]
    k=0
    while(2**k<1+len(vec)/10):
        bin_vec=2**k
        o=[]
        for _ in range(boot_cycle):
            temp=[]
            for _ in range(int(len(vec)/bin_vec)):
                i=rng.integers(0,len(vec))
                j=i
                while(j<len(vec) and j<i+bin_vec):
                    temp.append(vec[j])
                    j+=1
            o.append(osservabile(temp))
        bootk.append(np.std(o))
        k+=1
    return max(bootk)


def media_abs(vec, valass=False):
    if valass:
        return np.mean([abs(i) for i in vec])
    else:
        return np.mean(vec)

def varianza_abs(vec, valass=False):
    if valass:
        return np.var([abs(i) for i in vec])
    else:
        return np.var(vec)

def binder(vec):
    m2=0
    m4=0
    for i in vec:
        m2+=i**2/len(vec)
        m4+=i**4/len(vec)
    return m4/m2**2


def step( obj_reticolo, nstep=1000, nspazzate=10, nome = 1):
    '''
    nome= +1 se magnetizzazione, -1 se energia, 0 se entrambe
    Commento per noi: Per usare questa funzione per migliorare una storia montecarlo fare qualcosa tipo storia['ene'].extend(step['ene']) e storia['magn'].extend(step['magn'])
    '''
    vec = { 'ene' : [] , 'magn' : [] }
    if(nome == 1):
        for _ in range(nstep):
            obj_reticolo.aggiorna(nspazzate)
            vec['magn'].append(obj_reticolo.magn())
    elif(nome == -1):
        for _ in range(nstep):
            obj_reticolo.aggiorna(nspazzate)
            vec['ene'].append(obj_reticolo.energia())
    elif(nome == 0):
        for _ in range(nstep):
            obj_reticolo.aggiorna(nspazzate)
            vec['magn'].append(obj_reticolo.magn())
            vec['ene'].append(obj_reticolo.energia())
    else:
        print("Errore")
    return vec

def punto(vec, L, boot_cycle = 10,  nome='amag'):
    #calcola mag (magnetizzazione), amag (valore assoluto magnetizzazione), chi (suscettività), e (energia), c (calore specifico)
    res={}
    quant = nome in ['amag','chi','mag','binder']
    if(nome in ['amag','e','mag']):
        if(nome=='mag'):
            quant = False
        res['valore'] = media_abs(vec, quant)
        res['errore'] = bootstrap(lambda x: media_abs(x,quant), vec, boot_cycle=boot_cycle)
    elif(nome in ['c','chi']):
        res['valore'] = L*L*varianza_abs(vec, quant)
        res['errore'] = bootstrap( lambda x: L*L*varianza_abs(x, quant), vec, boot_cycle=boot_cycle)
    elif(nome=='binder'):
        res['valore'] = binder(vec)
        res['errore'] = bootstrap(binder, vec, boot_cycle=boot_cycle)
    else:
        print("Errore")
    return res






if __name__ == '__main__':
    lattice = ret.Reticolo(10, 0.3)
    print(lattice.mat)
    A = simulazione(lattice, nstep=100, nspazzate=10, nome='e', savehist=True)
    print(A)
    print(lattice.mat)

#prova:
#obj1 = Reticolo(8,0)
#obj1.aggiorna(beta=0.35,extfield=0,nspazzate=1)
#print('Il reticolo finale è')
#print(obj1.mat)
#print('La magnetizzazione è ', obj1.magn())
"""
beta=0.3
L=10
nstep=10000
nspazzate=100
bin=1
magn=punto(L,beta, 0, nstep,nspazzate,bin,'e')
print(magn['valore'],'+-', magn['errore'])


def step(obj_reticolo, nstep=1000, nspazzate=1, nome = 'amag'):#quant=True se si vuole prendere magnetizzazione o quant=False se si vuole prendere energia
    vec=[]
    #vorremmo fare fuori il controllo su quant
    quant = nome in ['amag','chi','mag']
    if quant:
        for _ in range(0,nstep):
            obj.aggiorna(nspazzate)
            vec.append(obj.magn())
    else:
        for _ in range(0,nstep):
            obj.aggiorna(nspazzate)
            vec.append(obj.energia())
    return vec
    

def punto(vec, L, boot_cycle = 10, bin_vec=1, nome='amag'): #calcola mag (magnetizzazione), amag (valore assoluto magnetizzazione), chi (suscettività), e (energia), c (calore specifico)
    res={}
    quant = nome in ['amag','chi','mag'] 
    if(nome in ['amag','e','mag']):
        if(nome=='mag'):
            quant = False
        res['valore'] = media_abs(vec, quant)
        res['errore'] = bootstrap(lambda x: media_abs(x,quant), vec, boot_cycle=boot_cycle, bin_vec=bin_vec)
    else:
        res['valore'] = L*L*varianza_abs(vec, quant)
        res['errore'] = bootstrap( lambda x: L*L*varianza_abs(x, quant), vec, boot_cycle=boot_cycle, bin_vec=bin_vec)
    return res

def absmagn_media(L=3, beta=0.30, extfield=0, step=1000, nspazzate=1): #funzione inutile.
    res=0
    obj = beta >= 0.44 and ret.Reticolo(L,1) or ret.Reticolo(L,0) #sotto la temperatura critica conviene partire da tutti spin up
    for _ in range(0,10): #termalizzazione
        obj.aggiorna(beta,extfield, nspazzate)
    for _ in range(0,step):
        for _ in range(0,nspazzate):
            obj.aggiorna(beta,extfield, nspazzate)
        res+=abs(obj.magn())
    return res/step
"""
#m=step(L,beta, 0, nstep,nspazzate,True)
#e=step(L,beta, 0, nstep,nspazzate,False)
#print('La media di |M| del reticolo con L=', L, 'a temperatura beta=', beta,'è', media_abs(m,True),'+-', bootstrap(lambda x: media_abs(x,True),m,bin))
#print('La suscettività del reticolo con L=', L, 'a temperatura beta=', beta,'è', L*L*varianza_abs(m,True),'+-', bootstrap(lambda x: L*L*varianza_abs(x, True),m,bin))
#print('La media dell energia  reticolo con L=', L, 'a temperatura beta=', beta,'è', media_abs(e),'+-', bootstrap(media_abs,e,bin))
#print('Il calore specifico del reticolo con L=', L, 'a temperatura beta=', beta,'è', L*L*varianza_abs(e),'+-', bootstrap(lambda x: L*L*varianza_abs(x),e,bin))

"""
def simulazione_old(obj_reticolo, nstep=1000, nspazzate=10, boot_cycle=10, nome = 'amag', savehist = False):
# calcola mag (magnetizzazione), amag (valore assoluto magnetizzazione), chi (suscettività), e (energia), c (calore specifico)
#Se savehis = False non salva la storia Montecarlo

    #if nome in ['storia_m','storia_e']:
    #    savehist = True
    vec=[]
    res={}
    quant = nome in ['amag','chi','mag','storia_m']
    if quant:
        for _ in range(nstep):
            obj_reticolo.aggiorna(nspazzate)
            vec.append(obj_reticolo.magn())
    else:
        for _ in range(nstep):
            obj_reticolo.aggiorna(nspazzate)
            vec.append(obj_reticolo.energia())

    if savehist:
        res['storia'] = vec.copy()

    if(nome in ['amag','e','mag']):
        if(nome=='mag'):
            quant = False
        res['valore'] = media_abs(vec, quant)
        res['errore'] = bootstrap(lambda x: media_abs(x,quant), vec, boot_cycle=boot_cycle)
    elif nome in ['chi', 'c']:
        res['valore'] = varianza_abs(vec, quant)*obj_reticolo.L**2
        res['errore'] = bootstrap( lambda x: varianza_abs(x, quant)*obj_reticolo.L**2, vec, boot_cycle=boot_cycle)
    return res"""
