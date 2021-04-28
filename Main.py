"""
Programma principale per la generazione di dati sul modello di Ising
"""

import numpy as np
from isinglib import ClasseReticolo
#from isinglib import bootstrap

beta = input("Inserisci la temperatura iniziale: ")
L = input("Inserisci la dimensione del reticolo: ")

ncamp = input("Inserisci il numero di misure: ")

bootstrap.printseed()

bootstrap.setseed(10)

bootstrap.printseed()

lattice = reticolo.Reticolo(L, 1)
print(lattice.mat)

print(lattice.__doc__)




