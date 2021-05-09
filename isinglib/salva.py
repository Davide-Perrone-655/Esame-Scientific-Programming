import numpy as np
import classe_reticolo as ret
import errors
import os
import sys


def salva_storia(obj_reticolo, nspazzate, vec, file_data):
    ''' funzione per salvare i dati e lo status della simulazione '''
    print('#L=%d' %obj_reticolo.L, file=file_data)
    print('#seed=%d' %10, file=file_data)
    print('#rngstatus=%s' %obj_reticolo.rng.bit_generator.state, file=file_data)
    print('#nspazzate=%d' %nspazzate, file=file_data)
    print('#beta=%f' %obj_reticolo.beta, file=file_data)
    print('#extfield=%f' %obj_reticolo.extfield, file=file_data)
    print('#MAT=', file=file_data)
    for i in obj_reticolo.mat:
        for j in i:
            if j==1:
                file_data.write('+')
            file_data.write(str(j)+' ')
        file_data.write('\n')
    for i in vec.keys():
        if( len(vec[i]) > 0 ):
            file_data.write( '#' + i + '=')
            for riga in vec[i]:
                file_data.write(str(riga)+ ' ')
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
        Attenzione: Niente doppi \n tra un dato e il successivo
    '''
    file_data.seek(0)
    opts={}
    line = file_data.readline()
    while( not line.startswith('#MAT=') ):
        s=line.split('=')
        if (isinstance(s[1], float)):
            opts[str(s[0][1:])] = float(s[1])
        elif (isinstance(s[1], int)):
            opts[str(s[0][1:])] = int(s[1])
        elif (isinstance(s[1], str)):
            opts[str(s[0][1:])] = str(s[1])
        else:
            raise errors.LoadError('Unsupported option type in %s' %file_data.name)
        line = file_data.readline()
        if not line.strip():
            raise errors.LoadError('#MAT not found in %s' %file_data.name)
    line = file_data.readline()
    opts['reticolo']=''
    while (not line.startswith('#magn=') and (not line.startswith('#ene=')) ):
        opts['reticolo']+=line
        line = file_data.readline()
        if not line.strip():
            raise errors.LoadError('Both #ene and #magn not found in %s' %file_data.name)
    opts['vec']={ 'ene': [] , 'magn': [] }
    while( bool(line.strip()) ):#eventuale end of file
        s=line.split('=')
        opts['vec'][str(s[0][1:])]=[float(i) for i in s[1].split()]
        line = file_data.readline()
    return opts

if __name__ == '__main__':
    lattice=ret.Reticolo(3, 0.3,conf_in=0, seed=10)
    lattice.aggiorna(1)
    print(lattice.mat)
    #file1=open('test', 'w')
    v={'magn': [0.1]}
    #salva_storia(lattice, 10, v, file1)
    #file1.close()
    file2=open('test','r')
    opt=reticolo_storia(file2)
    #print(opt['rngstatus'])
    lattice2=ret.Reticolo(3, 0.3,conf_in=0, seed=10)
    lattice2.init_rng(opt['rngstatus'])
    lattice2.aggiorna(1)
    print(lattice2.mat)
