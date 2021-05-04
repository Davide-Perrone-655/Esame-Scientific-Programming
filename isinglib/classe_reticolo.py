import numpy as np

class Reticolo():
    '''classe di un reticolo di ising 2D.'''
    # Constructor
    def __init__(self, L=None, conf_in=0):#conf_in=1 se spin tutti +1; -1 se tutti spin -1; altrimenti ogni spin +1 o -1 in modo random
        self.L = L
        self.conf_in = conf_in
        self.inizializza(L, conf_in)
       
    # Encapsulation!
    @property
    def L(self):
        '''Gets/sets numero di spin L.'''
        return self.__L

    @L.setter
    def L(self, val):
        self.__L = val

    @property
    def conf_in(self):
        return self.__conf_in

    @conf_in.setter
    def conf_in(self, val):
        self.__conf_in = val
    
    @property
    def mat(self):
        return self.__mat

    @mat.setter
    def mat(self, mat):
        self.__mat = mat
    
    # methods
    def inizializza(self, L=None, conf_in=1):
        '''Inizializza reticolo.'''
        if(conf_in==1):
            self.__mat = np.ones((L,L), dtype = int)
        elif(conf_in==-1):
            self.__mat = (-1)*np.np.ones((L,L), dtype = int)
        elif(conf_in==0):
            self.__mat=np.array([[-1+2*np.random.randint(2) for _ in range(L)] for _ in range(L)])
        elif(isinstance(conf_in, str)):
            self.L = conf_in.count('\n')
            self.__mat = np.array( [ [ int(i) for i in j.split() ] for j in conf_in.splitlines() ] )
        else:
            print('Errore')

        
    
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


if __name__ == '__main__':
    str1 = '1 -1 -1 1 -1 \n 1 -1 -1 -1 -1 \n +1 +1 +1 -1 1 \n 1 -1 -1 -1 -1 \n 1 -1 -1 1 -1 \n' 
    lattice = Reticolo(conf_in = str1)
    print(lattice.mat)
