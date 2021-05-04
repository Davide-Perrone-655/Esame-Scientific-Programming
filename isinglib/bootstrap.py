import time
from numpy.random import Generator, PCG64, MT19937

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

