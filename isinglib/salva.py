import numpy as np
from isinglib import classe_reticolo as ret
import os
import sys


def salva_storia(obj_reticolo, vec, file_data):
    ''' funzione per salvare i dati e lo status della simulazione '''
    print('#BETA=%f' %obj_reticolo.beta, file=file_data)
    print('#MAT=', file=file_data)
    for i in obj_reticolo.mat:
        for j in i:
            if j==1:
                file_data.write('+')
            file_data.write(str(j)+' ')
        file_data.write('\n')
    file_data.write('\n')
    for i in vec.keys():
        file_data.write( '#' + i.upper() + '=')
        for j in vec[i]:
            file_data.write(str(j)+ ' ')
        file_data.write('\n')
    file_data.write('\n')

def reticolo_storia(file_data):
    ''' funzione per salvare in una stringa il reticolo da dare poi in conf_in e poi il dizionario di ene e di magn'''
    file_data.seek(0)
    opts={}
    opts['L']=int(file_data.readline().split('=')[1])
    opts['seed']=int(file_data.readline().split('=')[1])
    line = file_data.readline()
    while not line.startswith('#BETA='):
        line = fobj.readline()
    opts['beta']=int(file_data.readline().split('=')[1])
    print('#BETA=%f' %obj_reticolo.beta, file=file_data)
    print('#MAT=', file=file_data)
    for i in obj_reticolo.mat:
        for j in i:
            if j==1:
                file_data.write('+')
            file_data.write(str(j)+' ')
        file_data.write('\n')
    file_data.write('\n')
    for i in vec.keys():
        file_data.write( '#' + i.upper() + '=')
        for j in vec[i]:
            file_data.write(str(j)+ ' ')
        file_data.write('\n')
    file_data.write('\n')
