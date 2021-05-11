import numpy as np
from isinglib import classe_reticolo as ret
from isinglib import errors
import os
import sys


def salva_storia(obj_reticolo, nspazzate, vec, file_data):
    ''' funzione per salvare i dati e lo status della simulazione '''
    print('#L=%d' %obj_reticolo.L, file=file_data)
    if obj_reticolo.seed == None:
        print('#seed=-1', file=file_data)
        print('#rngstatus={-1}' , file=file_data)
    else:
        print('#seed=%d' %obj_reticolo.seed, file=file_data)
        print('#rngstatus=%s' %obj_reticolo.rng.bit_generator.state , file=file_data)
    print('#nspazzate=%d' %nspazzate, file=file_data)
    print('#beta=%f' %obj_reticolo.beta, file=file_data)
    print('#extfield=%f' %obj_reticolo.extfield, file=file_data)
    print('#mat=', file=file_data)
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
    req_keys={'L','beta','seed','rngstatus','mat','nspazzate','extfield','vec'}
    file_data.seek(0)
    opts={}
    line = file_data.readline()

    while( not line.startswith('#mat=') ):

        if not line:
            raise errors.LoadError('#mat not found in "%s"' %file_data.name)
        
        if line.replace(' ','')=='\n':
            line = file_data.readline()
            
        if not line.strip().startswith('#'):
            raise errors.LoadError('Start token "#" not found, option not recognized in "%s"' %file_data.name)

        s=line.strip().split('=')
        if (s[1].startswith('{')):
            opts[s[0][1:]] = s[1]
        elif ('.' in s[1]):
            try:
                opts[s[0][1:]] = float(s[1])
            except ValueError:
                raise errors.LoadError('Unexpected value in %s' %s[0][1:])
        else:
            try:
                opts[s[0][1:]] = int(s[1])
            except ValueError:
                raise errors.LoadError('Unexpected value in %s' %s[0][1:])
        line = file_data.readline()

    line = file_data.readline()
    opts['mat']=''
    while ( (not line.startswith('#magn=')) and (not line.startswith('#ene=')) and line):
        opts['mat']+=line
        line = file_data.readline()
    opts['vec']={ 'ene': [] , 'magn': [] }

    while(line):
        if (line.replace(' ','')!='\n' and line.strip().startswith('#')):
            try:
                s=line.split('=')
                opts['vec'][s[0][1:]]=[float(i) for i in s[1].split()]
            except ValueError:
                raise errors.LoadError('Error in converting #magn or #ene datas in "%s"' %file_data.name)
        line = file_data.readline()

    if set(opts.keys()) == req_keys:
        if opts['seed']==-1:
            opts['seed'] = None 
        if opts['rngstatus'] == '{-1}':
            opts['rngstatus'] = None
        return opts
    else:
        miss_keys = req_keys - set(opts.keys())
        raise errors.LoadError('Required key(s) %s missing in "%s"' %(miss_keys, file_data.name))

if __name__ == '__main__':
    lattice=ret.Reticolo(5, 0.2, conf_in=0)
    lattice.aggiorna(1)
    #print(lattice.mat)
    file1=open('test', 'w')
    #v={'magn': [0.1]}
    salva_storia(lattice, 10, {}, file1)
    file1.close()
    file2=open('test','r')
    opt=reticolo_storia(file2)
    #print(opt['mat'])
    #print(opt['rngstatus'])
    print('\n')
    lattice2=ret.Reticolo(5, 0.2, term=0, conf_in=opt['mat'])
    #lattice2.aggiorna(1)
    print(lattice2.seed)
    print('carico il gen')
    #lattice2.init_rng(opt['rngstatus'])
    #lattice2.aggiorna(1)
    #lattice.aggiorna(1)
    #print(lattice.mat)
    print('\n')
    #print(lattice2.mat)
    
   
