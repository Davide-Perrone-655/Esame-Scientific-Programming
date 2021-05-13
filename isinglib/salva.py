from isinglib import errors
import os





def func_save(L, h, x_name, x_axis, d_oss, nome_outf, fpath):
    file_data = open(fpath+os.sep+nome_outf, 'w')
    print('#L={}'.format(L),file=file_data)
    print('#extfield={:.8f}'.format(h),file=file_data)
    fmt='#{}\t\t'.format(x_name)
    for oss in d_oss.keys():
        fmt+='#{s}\t\t#d{s}\t\t'.format(s=oss)
    print(fmt.strip(),file=file_data)
    for i, x in enumerate(x_axis):
        fmt='{:.8f}\t'.format(x)
        for oss in d_oss.keys():
            fmt+='{:.8f}\t{:.8f}\t'.format(d_oss[oss]['valore'][i],d_oss[oss]['errore'][i])
        print(fmt.strip(),file=file_data)
    file_data.close()



def read_data(out_file):
    ''' funzione per leggere i risultati della simulazione '''
    file_data=open(out_file,'r')
    L = int(file_data.readline().strip().split('=')[1])
    h = float(file_data.readline().strip().split('=')[1])
    s = file_data.readline().strip().split()
    unitx = s[0][1:]
    oss_list = [ word[1:].lstrip('d') for word in s[1:] ]
    x_axis=[]
    d_oss = { oss : {'valore': [], 'errore': []} for oss in oss_list }
    line=file_data.readline().strip()
    while(line):
        s = line.split()
        x_axis.append(float(s[0]))
        type = 'valore'
        for name, val in zip(oss_list, s[1:]):
            d_oss[name][type].append(float(val))
            type = type == 'valore' and 'errore' or 'valore'
        line=file_data.readline().strip()
    datas = {'x_axis': x_axis, 'd_oss': d_oss, 'L': L, 'extfield': h, 'unitx': unitx}
    return datas


def salva_storia(obj_reticolo, vec, file_data):
    ''' funzione per salvare i dati e lo status della simulazione '''
    print('#L=%d' %obj_reticolo.L, file=file_data)
    if obj_reticolo.seed == None:
        print('#seed=-1', file=file_data)
        print('#rngstatus={-1}' , file=file_data)
    else:
        print('#seed=%d' %obj_reticolo.seed, file=file_data)
        print('#rngstatus=%s' %obj_reticolo.rng.bit_generator.state , file=file_data)
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

def gread(file_data):
    line = file_data.readline()
    while not line.strip():
        line = file_data.readline()
    return line



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
    req_keys={'L','beta','seed','rngstatus','mat','extfield','vec'}
    req_keys_1=['L','seed','rngstatus','beta','extfield']
    file_data.seek(0)
    opts={}
    conv_func = [int, int, str, float, float]
    line = gread(file_data)
    
    for key, conv in zip(req_keys_1, conv_func):
        try:
            s = line.split('=')
            if s[0].strip()[1:] != key:
                raise errors.LoadError('Unexpected parameter "{}" Expected parameter: "{}"'.format(s[0].strip()[1:], key))
            opts[key] = conv(s[1].strip())
        except ValueError:
            raise errors.LoadError('{} from {}'.format(key, file_data.name))

        line = gread(file_data)
    line = gread(file_data)

    opts['mat']=''
    while ( line and not(line.startswith('#magn=') or line.startswith('#ene=')) ):
        opts['mat']+=line
        line = file_data.readline()

    opts['vec']={ 'ene': [] , 'magn': [] }
    while(line):
        if (line.replace(' ','')!='\n' and line.strip().startswith('#')):
            try:
                s=line.split('=')
                opts['vec'][s[0][1:]]=[float(i) for i in s[1].split()]
            except ValueError:
                raise errors.LoadError('Error in converting #magn or #ene datas')
        line = file_data.readline()

    
    if opts['seed']==-1:
        opts['seed'] = None 
    if opts['rngstatus'] == '{-1}':
        opts['rngstatus'] = None
    return opts


    
   
