import numpy as np
from isinglib import classe_reticolo as ret
import os
import sys


def salva_storia(obj_reticolo, vec, file_data):
    ''' funzione per salvare i dati e lo status della simulazione '''
    print('#BETA=%f' %obj_reticolo.beta, file=file_data)
    print('#MAT=', file=file_data)
    for i in obj_reticolo.mat:
        file_data.write(str(i) + '\n')
    file_data.write('\n')
    for i in vec.keys():
        file_data.write( '#' + i.upper() + '=')
        for j in vec[i]:
            file_data.write(str(j)+ ' ')
        file_data.write('\n')
    file_data.write('\n')