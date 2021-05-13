'''Additional class defined to handle MonteCarlo evolution of a lattice'''
from numpy.random import Generator, PCG64
from isinglib import errors
#import errors
import numpy as np
import re



class Reticolo():
    '''
    2D ising lattice running with Metropolis algorithm

    Attributes:

    L -> lattice dimension 
    beta -> temperature (1/T) of current simulation
    extfield -> external field
    term -> termalization time. This attribute forces an update of the lattice matrix during initialization in order to termalize, eg term=3: 3 full lattice updates. If -1 given, uses a standard termalization time: L**2
    conf_in -> [1,0,-1, str] Initial lattice configuration: +1 all spins up, -1 all spins down, 0 all spins random. If it is a string, tries to unpack and load the given lattice configuration
    seed -> RNG seed
    state -> RNG starting state
    gexp -> contains the generated exponentials 

    Methods:
    init_rng() -> initialize the Generator class, with a given state
    gen_exp() -> generates the exponentials required to accept/reject the MonteCarlo proposed change
    inizializza() -> initialize a lattice with a given dimension L and configuration, also termalizing it at the given temperature beta
    update_metropolis() -> runs L**2 calls of local metropolis algorithm
    magn(), ene() -> returns energy or magnetization of the current lattice configuration
    '''
    # Constructor
    def __init__(self, L, beta, term = -1, extfield = 0, conf_in = None, seed = None, state = None):
        self.__seed = seed
        self.rng = Generator(PCG64(seed))
        self.init_rng(state)

        #if no configuration given, the lattice is initialized with broken symmetry if beta is higher than the critical beta,
        # in order to minimize the termalization time
        if conf_in == None:
            conf_in = (beta>=0.44) and 1 or 0

        self.__L = L
        self.gen_exp(beta, extfield)
        self.inizializza(L, term, conf_in)
    
    # Encapsulation
    @property
    def beta(self):
        return self.__beta
    
    @property
    def extfield(self):
        return self.__extfield
    
    @property
    def seed(self):
        return self.__seed
    
    @seed.setter
    def seed(self, val):
        self.__seed = val
        self.rng = Generator(PCG64(val))

    @property
    def mat(self):
        return self.__mat

    @mat.setter
    def mat(self, mat):
        self.__mat = mat
    
    @property
    def L(self):
        return self.__L


    # methods
    def init_rng(self, state):
        if state !=None:
            #pattern required to unpack the generator state
            pattern = re.compile(r'''(?:^\{)(\w+)(?:\:\s+)(\w+)(?:,\s+)(\w+)(?:\:\s+\{)(\w+)(?:\:\s+)
            (\d+)(?:,\s+)(\w+)(?:\:\s+)(\d+)(?:\},\s+)(\w+)(?:\:\s+)(\d+)(?:,\s+)(\w+)(?:\:\s+)(\d+)(?:}$)''')
            
            if pattern.match(state.replace("'",'')):
                s_init = pattern.search(state.replace("'",'')).groups()
                #the generator state is passed to bit_generator.state as a dictionary
                state = { s_init[0]: s_init[1], s_init[2] : {s_init[3] : int(s_init[4]), s_init[5] : int(s_init[6])}, s_init[7] : int(s_init[8]), s_init[9] : int(s_init[10])}
                self.rng.bit_generator.state = state
            else:
                raise errors.InitializationError('Incorrect generator state, pattern mismatch')

    def gen_exp(self, beta, extfield = 0):
        #setting the results to 1.0 has been done in order to avoid overflows in exponential calculation, for high values of beta
        self.__gexp = { s : {f :  s*(f + extfield)<=0 and 1.0 or np.exp(-2*beta*s*(f + extfield)) for f in range(-4, 6, 2)} for s in [+1, -1]}
        self.__beta = beta
        self.__extfield = extfield

    def update_metropolis(self, nspazzate = 1): 
        for _ in range(nspazzate*self.__L**2):
            i=self.rng.integers(0,self.__L)
            j=self.rng.integers(0,self.__L)
            force = self.__mat[i][(j-1)%self.__L] + self.__mat[i][(j+1)%self.__L] + self.__mat[(i-1)%self.__L][j] + self.__mat[(i+1)%self.__L][j]
            #Metropolis test, accept/reject changes
            if self.rng.random()<self.__gexp[self.__mat[i][j]][force] :
                self.__mat[i][j]*=-1




    def inizializza(self, L, term=-1, conf_in=1):
        #initialize lattice
        if (not isinstance(L, int)) or L <=0:
            raise errors.InitializationError('Lattice must have a positive integer dimension')

        if(conf_in==1):
           self.__mat = np.ones((L,L), dtype = int)
        elif(conf_in==-1):
            self.__mat = (-1)*np.ones((L,L), dtype = int)
        elif(conf_in==0):
            self.__mat=np.array([[-1+2*self.rng.integers(0,2) for _ in range(L)] for _ in range(L)])
            
        elif(isinstance(conf_in, str)):
            #configuration pattern
            conf_out = conf_in.replace('\n','').replace(' ','').replace('1', '1 ')
            pattern = re.compile(r'(?:^)([\+-]?1\s){' + str(L*L) + r'}(?:$)')

            if pattern.match(conf_out):
                #self.__mat = np.array(conf_out.split(), dtype=int).reshape(L,L)
                self.__mat = np.array( [ [ int(i) for i in conf_out.split()[j*L:(j+1)*L] ] for j in range(L) ] )
            else:
                raise errors.InitializationError('Incorrect imported matrix\n%s' %conf_in)

        else:
            raise errors.InitializationError('Initial configuration not recognized. Choose between [-1, 0, +1, str]')

        if term==-1:
            term = L*L 
        if (not isinstance(term, int)) or term < 0:
            raise errors.InitializationError('Termalization time must be a positive integer')
        self.update_metropolis(term)



    def magn(self):
        return np.mean(self.__mat)
    
    def energia(self):
        xene = 0
        for i in range(self.__L):
            for j in range(self.__L):
                xene -= 0.5*self.__mat[i][j]*(self.__mat[i][(j-1)%self.__L] + self.__mat[i][(j+1)%self.__L] + self.__mat[(i-1)%self.__L][j] + self.__mat[(i+1)%self.__L][j]) + self.__extfield*self.__mat[i][j]
        return xene/self.__L**2
    


if __name__ == '__main__':
    print(Reticolo.__doc__)