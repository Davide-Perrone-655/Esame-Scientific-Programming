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
        '''Gets/sets numero di spin L.'''
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


#prova:
obj1 = Reticolo(8,0)
obj1.aggiorna(beta=0.35,extfield=0,nspazzate=1)
print('Il reticolo finale è')
print(obj1.mat)
print('La magnetizzazione è ', obj1.magn())
print('L\'energia è ', obj1.energia(extfield=0))
