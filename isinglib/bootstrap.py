import numpy as np

rng = np.random.default_rng()

def bootstrap(osservabile, vec, boot_cycle = 10):
    bootk=[]
    len_vec=len(vec)
    bin_vec = 1+len_vec//1000
    while(bin_vec<=1+len_vec/10):
        o=[]
        for _ in range(boot_cycle):
            temp=[]
            for _ in range(int(len_vec/bin_vec)):
                i=rng.integers(len_vec)
                temp.extend(vec[i:min(i+bin_vec,len_vec)])
                
            o.append(osservabile(temp))
        bootk.append(np.std(o))
        bin_vec*=2
    return max(bootk)


def find_matter(oss):
    if oss in {'amag','chi','mag','binder'} :
        return 'magn'
    return 'ene'


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


def step( obj_reticolo, nstep=1000, nome = 1):
    '''
    nome= +1 se magnetizzazione, -1 se energia, 0 se entrambe
    Commento per noi: Per usare questa funzione per migliorare una storia montecarlo fare qualcosa tipo storia['ene'].extend(step['ene']) e storia['magn'].extend(step['magn'])
    '''
    vec = { 'ene' : [] , 'magn' : [] }
    if(nome == 1):
        for _ in range(nstep):
            obj_reticolo.update_metropolis()
            
            vec['magn'].append(obj_reticolo.magn())
    elif(nome == -1):
        for _ in range(nstep):
            obj_reticolo.update_metropolis()
            vec['ene'].append(obj_reticolo.energia())
    elif(nome == 0):
        for _ in range(nstep):
            obj_reticolo.update_metropolis()
            vec['magn'].append(obj_reticolo.magn())
            vec['ene'].append(obj_reticolo.energia())
    else:
        print("Errore step")
    return vec

def punto(vec, L,  nome='amag'):
    #calcola mag (magnetizzazione), amag (valore assoluto magnetizzazione), chi (suscettività), e (energia), c (calore specifico)
    res={}
    quant = nome in ['amag','chi','mag','binder']
    if(nome in ['amag','ene','mag']):
        if(nome=='mag'):
            quant = False
        res['valore'] = media_abs(vec, quant)
        print(res['valore'])
        res['errore'] = bootstrap(lambda x: media_abs(x,quant), vec)
    elif(nome in ['c','chi']):
        res['valore'] = L*L*varianza_abs(vec, quant)
        res['errore'] = bootstrap( lambda x: L*L*varianza_abs(x, quant), vec)
    elif(nome=='binder'):
        res['valore'] = binder(vec)
        res['errore'] = bootstrap(binder, vec)
    else:
        print("Errore")
    return res

