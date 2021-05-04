import time
import numpy as np
from numpy.random import Generator, PCG64, MT19937
from isinglib import classe_reticolo as ret

#non so se vada bene usare global, però non ho trovato altri modi. Andrebbe testato meglio

def setseed(a):
	'''Imposta il seed ad un valore scelto. Default: orario attuale'''

	global seed
	seed = a
	print('seed: %d' %seed)



seed = time.time_ns()


def printseed():
    '''Funzione per stampare il seed, è solo un controllo'''
    print(seed)


'''
Generatore di numeri casuali : PCG64 o Mersenne Twister (per ora PCG64)
'''
rg=Generator(PCG64(seed))



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

def bootstrap(osservabile, vec, bin=1):
    media=0
    media2=0
    for _ in range(0,100):
        temp=[]
        for _ in range(int(len(vec)/bin)):
            i=np.random.randint(len(vec))
            j=i
            while(j<len(vec) and j<i+bin):
                temp.append(vec[j])
                j+=1
        o=osservabile(temp)
        media+=o
        media2+=o*o
    media/=100
    media2/=100
    return np.sqrt(media2-media*media)
    
def media_abs(vec, valass=False):
    f= valass == True and abs or (lambda x: x)
    return sum([f(i) for i in vec])/len(vec)

def varianza_abs(vec, valass=False):
    f= valass == True and abs or (lambda x: x)
    media=0
    media2=0
    for a in vec:
        media+= f(a)
        media2+=a*a
    media/=len(vec)
    media2/=len(vec)
    return media2-media*media



def step(L=3, beta=0.30, extfield=0, nstep=1000, nspazzate=1, quant=True):#quant=True se si vuole prendere magnetizzazione o quant=False se si vuole prendere energia
    vec=[]
    obj = beta >= 0.44 and ret.Reticolo(L,1) or ret.Reticolo(L,0) #sotto la temperatura critica conviene partire da tutti spin up
    for _ in range(0,10): #termalizzazione
        obj.aggiorna(beta, extfield, nspazzate)
    for _ in range(0,nstep):
        for _ in range(0,nspazzate):
            obj.aggiorna(beta, extfield, nspazzate)
        if quant:
            vec.append(obj.magn())
        else:
            vec.append(obj.energia())
    return vec
    

def punto(L, beta, extfield=0, nstep=1000, nspazzate=1, bin=1, nome='|m|'): #calcola m (magnetizzazione), |m| (valore assoluto magnetizzazione), chi (suscettività), e (energia), c (calore specifico)
    res={}
    b= (nome in ['|m|','chi','m'] )
    v=step(L,beta, extfield, nstep,nspazzate,b)
    if(nome in ['|m|','e','m']):
        if(nome=='m'):
            b=False
        res['valore'] = media_abs(v,b)
        res['errore'] = bootstrap(lambda x: media_abs(x,b),v,bin)
    else:
        res['valore'] = L*L*varianza_abs(v,b)
        res['errore'] = bootstrap( lambda x: L*L*varianza_abs(x, b) ,v,bin)
    return res
    
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
"""
#m=step(L,beta, 0, nstep,nspazzate,True)
#e=step(L,beta, 0, nstep,nspazzate,False)
#print('La media di |M| del reticolo con L=', L, 'a temperatura beta=', beta,'è', media_abs(m,True),'+-', bootstrap(lambda x: media_abs(x,True),m,bin))
#print('La suscettività del reticolo con L=', L, 'a temperatura beta=', beta,'è', L*L*varianza_abs(m,True),'+-', bootstrap(lambda x: L*L*varianza_abs(x, True),m,bin))
#print('La media dell energia  reticolo con L=', L, 'a temperatura beta=', beta,'è', media_abs(e),'+-', bootstrap(media_abs,e,bin))
#print('Il calore specifico del reticolo con L=', L, 'a temperatura beta=', beta,'è', L*L*varianza_abs(e),'+-', bootstrap(lambda x: L*L*varianza_abs(x),e,bin))


