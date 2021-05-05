import numpy as np
import time

class Reticolo():
    '''classe di un reticolo di ising 2D.'''
    # Constructor
    def __init__(self, L, beta, extfield=0, conf_in=0):#conf_in=1 se spin tutti +1; -1 se tutti spin -1; altrimenti ogni spin +1 o -1 in modo random
        self.__L = L
        self.inizializza(L, conf_in)
        self.gen_exp(beta, extfield)

    # Encapsulation
    @property
    def mat(self):
        return self.__mat

    @mat.setter
    def mat(self, mat):
        self.__mat = mat
    
    # methods
    def gen_exp(self, beta, extfield):
        self.__gexp = { s : {f : np.exp(-2*beta*s*(f + extfield)) for f in range(-4, 6, 2)} for s in [+1, -1]}
        self.__beta = beta
        self.__extfield = extfield


    def inizializza(self, L=None, conf_in=1):
        '''Inizializza reticolo.'''
        if(conf_in==1):
            self.__mat = np.ones((L,L), dtype = int)
        elif(conf_in==-1):
            self.__mat = (-1)*np.np.ones((L,L), dtype = int)
        elif(conf_in==0):
            self.__mat=np.array([[-1+2*np.random.randint(2) for _ in range(L)] for _ in range(L)])
        elif(isinstance(conf_in, str)):
            self.__L = conf_in.count('\n')
            self.__mat = np.array( [ [ int(i) for i in j.split() ] for j in conf_in.splitlines() ] )
            #occhio, si ragiona al contrario con i cicli innestati
        else:
            print('Errore')


    def magn(self):
        return np.mean(self.__mat)
    
    def energia(self):
        xene = 0
        for i in range(self.__L):
            for j in range(self.__L):
                xene -= 0.5*self.__mat[i][j]*(self.__mat[i][(j-1)%self.__L] + self.__mat[i][(j+1)%self.__L] + self.__mat[(i-1)%self.__L][j] + self.__mat[(i+1)%self.__L][j]) + self.__extfield*self.__mat[i][j]
        return xene/self.__L**2
    
    def aggiorna(self, nspazzate=10):
        for _ in range(nspazzate*self.__L**2):
            i=np.random.randint(self.__L)
            j=np.random.randint(self.__L)
            force = self.__mat[i][(j-1)%self.__L] + self.__mat[i][(j+1)%self.__L] + self.__mat[(i-1)%self.__L][j] + self.__mat[(i+1)%self.__L][j]
            if np.random.random()<self.__gexp[self.__mat[i][j]][force] :
                self.__mat[i][j]*=-1


if __name__ == '__main__':
    str1 = '1 -1 -1 1 -1 \n 1 -1 -1 -1 -1 \n +1 +1 +1 -1 1 \n 1 -1 -1 -1 -1 \n 1 -1 -1 1 -1 \n'
    print(str1)
    #lattice = Reticolo(conf_in = str1)
    lattice = Reticolo(10, 0.3)
    print(lattice.mat)
    start = time.process_time()
    lattice.aggiorna(100)
    eps = (time.process_time() - start)/100
    print(eps)
    print(lattice.mat)
    print(eps*100*10000)
    ene = 0
    mag = 0
    for _ in range(10000):
        lattice.aggiorna(100)
        ene += lattice.energia()
        mag += lattice.magn()
    ene = ene/10000
    mag = mag/10000
    print(ene)
    print(mag)
    print(time.process_time() - start)

"""
    @property
    def conf_in(self):
        return self.__conf_in

    @conf_in.setter
    def conf_in(self, val):
        self.__conf_in = val
    

    @property
    def L(self):
        '''Gets/sets numero di spin L.'''
        return self.__L
    @L.setter
    def L(self, val):
        self.__L = val

    @property
    def beta(self):
        return self.__beta
    @beta.setter
    def beta(self, val):
        self.__beta = val

    @property
    def extfield(self):
        return self.__extfield
    @extfield.setter
    def extfield(self, val):
        self.__extfield = val
    
    @property
    def gexp(self):
        return self.__gexp
    @gexp.setter
    def gexp(self, val):
        self.__gexp = val

"""