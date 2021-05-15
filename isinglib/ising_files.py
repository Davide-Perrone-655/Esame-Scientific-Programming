'''Module to handle files'''

from isinglib import ising_errors as errors
from isinglib import ising_lattice as ret
from isinglib import ising_type
import typing as tp
import os



def func_save(L: int, h: float, x_name: str, x_axis: tp.List[float], d_oss: tp.Dict[str, tp.Dict[str, float]], nome_outf: str, fpath: str) -> tp.NoReturn:
    '''Function to save observable(s) results '''
    file_data = open(fpath+os.sep+nome_outf, 'w')
    print('#L={}'.format(L),file=file_data)
    print('#extfield={:.8f}'.format(h),file=file_data)

    #Tries to make columns of datas
    fmt='#{}\t\t'.format(x_name)
    for oss in d_oss.keys():
        fmt += '#{s}\t\t#d{s}\t\t'.format(s=oss)
    print(fmt.strip(),file=file_data)

    #Print datas on file, spaced with tab and with 8 digit precision
    for i, x in enumerate(x_axis):
        fmt = '{:.8f}\t'.format(x)
        for oss in d_oss.keys():
            fmt += '{:.8f}\t{:.8f}\t'.format(d_oss[oss]['valore'][i], d_oss[oss]['errore'][i])
        print(fmt.strip(),file=file_data)
    file_data.close()



def read_data(out_file: str) -> ising_type.tpoutdata:
    '''Function to read data from the output file of observable(s) calculation(s)'''
    file_data=open(out_file,'r')
    
    #Reads L, extfield
    L = int(file_data.readline().strip().split('=')[1])
    h = float(file_data.readline().strip().split('=')[1])

    #Reads the line with beta, observables and uncertainties
    s = file_data.readline().strip().split()

    #Exclude the first charachter in file: #
    unitx = s[0][1:]
    oss_list = [ word[1:].lstrip('d') for word in s[1:] ]
    x_axis=[]

    #Create the dictionary of values and errors for every observable in the file
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
    
    #Creating the dictionary with all the information loaded
    datas = {'x_axis': x_axis, 'd_oss': d_oss, 'L': L, 'extfield': h, 'unitx': unitx}
    return datas



def salva_storia(obj_reticolo: tp.Type[ret.Reticolo], vec: tp.Dict[str,tp.Dict[str, float]], file_name: str) -> tp.NoReturn:
    '''Function to save a single MC story '''

    file_data = open(file_name, 'w')
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

    #Saving final matrix configuration
    for i in obj_reticolo.mat:
        for j in i:
            file_data.write('{:+d} '.format(j))
        file_data.write('\n')
    
    #Saving energy and/or magnetization
    for i in vec.keys():
        if( len(vec[i]) > 0 ):
            file_data.write( '#' + i + '=')
            for riga in vec[i]:
                file_data.write(str(riga)+ ' ')
            file_data.write('\n')
    file_data.close()



def gread(file_data: tp.TextIO) -> tp.TextIO:
    '''Read lines, skipping the empty ones'''
    line = file_data.readline()
    while not line.strip():
        line = file_data.readline()
    return line



def reticolo_storia(file_data: tp.TextIO) -> ising_type.tpopt:
    '''Function to save datas in a dictionary. File must contains:  
        #L=int
        #seed=int
        #rngstatus=str
        #beta=float
        #extfield=float
        #MAT=
        lattice
        #ene(or magn)= ..
        #ene(or/and magn)= ..'''
    
    req_keys_1=['L','seed','rngstatus','beta','extfield']
    file_data.seek(0)
    opts={}
    conv_func = [int, int, str, float, float]
    line = gread(file_data)
    
    #Reads until matrix
    for key, conv in zip(req_keys_1, conv_func):
        try:
            s = line.split('=')
            if s[0].strip()[1:] != key:
                raise errors.LoadError('Unexpected parameter "{}". Expected parameter: "{}"'.format(s[0].strip()[1:], key))
            opts[key] = conv(s[1].strip())
        except ValueError:
            raise errors.LoadError('{} from {}'.format(key, file_data.name))

        line = gread(file_data)
    #Reads the matrix, removing #mat line
    line = gread(file_data)
    opts['mat']=''
    while ( line and not(line.startswith('#magn=') or line.startswith('#ene=')) ):
        opts['mat']+=line
        line = file_data.readline()

    #Reads data
    opts['vec']={ 'ene': [] , 'magn': [] }
    while(line):
        if (line.replace(' ','')!='\n' and line.strip().startswith('#')):
            try:
                s=line.split('=')
                opts['vec'][s[0][1:]]=[float(i) for i in s[1].split()]
            except ValueError:
                raise errors.LoadError('Error in converting #magn or #ene datas')
        line = file_data.readline()

    #set default seed and rngstatus if None needed    
    if opts['seed']==-1:
        opts['seed'] = None 
    if opts['rngstatus'] == '{-1}':
        opts['rngstatus'] = None
    return opts


    
   
