import numpy as np
from isinglib import classe_reticolo as ret
import os
import sys


def salva_storia(obj_reticolo, vec, file_data):
    ''' funzione per salvare i dati e lo status della simulazione '''
    print('#beta=%f' %obj_reticolo.beta, file=file_data)
    print('#MAT=', file=file_data)
    for i in obj_reticolo.mat:
        for j in i:
            if j==1:
                file_data.write('+')
            file_data.write(str(j)+' ')
        file_data.write('\n')
    for i in vec.keys():
        if( len(vec[i]) > 0 ):
            file_data.write( '#' + i.upper() + '=')
            for j in vec[i]:
                file_data.write(str(j)+ ' ')
            file_data.write('\n')

def reticolo_storia(file_data):
    ''' funzione per salvare i dati dal file in un dizionario. Il file di lettura deve essere costruito nel seguente modo:
        #dato_1=valore_1
        ..
        #dato_k=valore_k
        #MAT=
         reticolo
        #ene(o magn)= ..
        #ene(o/e magn)= ..
    '''
    file_data.seek(0)
    opts={}
    line = file_data.readline()
    while( not line.startswith('#MAT=') ):
        s=line.split('=')
        opts[str(s[0][1:])]= '.' in s[1] and float(s[1]) or int(s[1])
        line = file_data.readline()
    line = file_data.readline()
    opts['reticolo']=''
    while (not line.startswith('#magn=') and not line.startswith('#ene=')):
        opts['reticolo']+=line
        line = file_data.readline()
    opts['vec']={ 'ene': [] , 'magn': [] }
    while( bool(line.strip()) ):
        s=line.split('=')
        opts['vec'][str(s[0][1:])]=[float(i) for i in s[1].split()]
        line = file_data.readline()
    return opts
