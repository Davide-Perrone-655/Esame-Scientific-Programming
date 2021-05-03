import numpy as np

class Reticolo():
    '''classe di un reticolo di ising 2D.'''
    # Constructor
    def __init__(self, L=5, conf_in=1):#conf_in=1 se spin tutti +1; -1 se tutti spin -1; altrimenti ogni spin +1 o -1 in modo random
        self.L=L
        self.conf_in=int(conf_in)
        self.inizializza(L,conf_in)
        
    # Encapsulation
    @property
    def L(self):
        '''Gets/sets numero di spin L.'''
        return self.__L

    @L.setter
    def L(self, val):
        self.__L = int(val)

    @property
    def conf_in(self):
        return self.__conf_in

    @conf_in.setter
    def conf_in(self, val):
        self.__conf_in = int(val)
    
    @property
    def mat(self):
        return self.__mat

    @mat.setter
    def mat(self, mat):
        self.__mat =mat
    
    # methods
    def inizializza(self, L, conf_in):
        '''Inizializza reticolo.'''
        if(conf_in==1):
            self.__mat=np.array(L*[L*[1]])
        elif(conf_in==-1):
            self.__mat=np.array(L*[L*[-1]])
        else:
            self.__mat=np.array([[-1+2*np.random.randint(2) for _ in range(0,L)] for _ in range(0,L)])
    
    def magn(self):
        return self.__mat.sum()/self.__L**2
    
    def energia(self,extfield=0):
        xene=0
        for i in range(self.__L):
            for j in range(self.__L):
                xene-=0.5*self.__mat[i][j]*(self.__mat[i][(j-1)%self.__L] + self.__mat[i][(j+1)%self.__L] + self.__mat[(i-1)%self.__L][j] + self.__mat[(i+1)%self.__L][j])+extfield*self.__mat[i][j]
        return xene/self.__L**2
    
    def aggiorna(self, beta=0.30, extfield=0, nspazzate=100):
        for _ in range(nspazzate*self.__L**2):
            i=np.random.randint(self.__L)
            j=np.random.randint(self.__L)
            force= self.__mat[i][(j-1)%self.__L] + self.__mat[i][(j+1)%self.__L] + self.__mat[(i-1)%self.__L][j] + self.__mat[(i+1)%self.__L][j]
            if np.random.random()<np.exp(-2*beta*self.__mat[i][j]*(force+extfield)) :
                self.__mat[i][j]*=-1

def absmagn_media(L=3, beta=0.30, extfield=0, step=1000, nspazzate=1): #funzione inutile.
    res=0
    obj = beta >= 0.44 and Reticolo(L,1) or Reticolo(L,0) #sotto la temperatura critica conviene partire da tutti spin up
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
    obj = beta >= 0.44 and Reticolo(L,1) or Reticolo(L,0) #sotto la temperatura critica conviene partire da tutti spin up
    for _ in range(0,10): #termalizzazione
        obj.aggiorna(beta,extfield, nspazzate)
    for _ in range(0,nstep):
        for _ in range(0,nspazzate):
            obj.aggiorna(beta,extfield, nspazzate)
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
beta=0.35
L=10
nstep=200
nspazzate=1
bin=50
magn=punto(L,beta, 0, nstep,nspazzate,bin,'m')
print(magn['valore'],'+-', magn['errore'])
#m=step(L,beta, 0, nstep,nspazzate,True)
#e=step(L,beta, 0, nstep,nspazzate,False)
#print('La media di |M| del reticolo con L=', L, 'a temperatura beta=', beta,'è', media_abs(m,True),'+-', bootstrap(lambda x: media_abs(x,True),m,bin))
#print('La suscettività del reticolo con L=', L, 'a temperatura beta=', beta,'è', L*L*varianza_abs(m,True),'+-', bootstrap(lambda x: L*L*varianza_abs(x, True),m,bin))
#print('La media dell energia  reticolo con L=', L, 'a temperatura beta=', beta,'è', media_abs(e),'+-', bootstrap(media_abs,e,bin))
#print('Il calore specifico del reticolo con L=', L, 'a temperatura beta=', beta,'è', L*L*varianza_abs(e),'+-', bootstrap(lambda x: L*L*varianza_abs(x),e,bin))
