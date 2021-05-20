#!/usr/bin/env python3

'''Plot function and mode 2 plotting'''

from isinglib import ising_files as salva
from isinglib import ising_small as sml
import matplotlib.pyplot as plt
import typing as tp
import os


def plot_graph(x: tp.List[float], y: tp.List[float], dy: tp.List[float], L: int , h: float, nome_x: str, nome_y: str, block_fig = True) -> tp.NoReturn:
    '''Graph plotter with tex labels'''
    latex_xname = {'beta': '$\u03b2$', 'T': '$T$'}
    latex_yname = {'c': ['$C$', 'specific heat'], 'chi': ['$\chi$', 'magnetic susceptibility'], 'ene': ['$\epsilon$', 'mean energy'], 'binder': ['$B$', 'binder cumulant'], 'mag': ['$M$', 'mean magnetization'], 'amag': ['$|M|$','mean absolute value of magnetization']}
    title = '{}, L={:d}, h={:.3f}'.format(latex_yname[nome_y][1].title(), L, h)

    fig = plt.figure(figsize = (12, 8), dpi=92)
    ax = plt.subplot(1,1,1)

    ax.errorbar(x, y, dy,  marker = '.')
    ax.set_title( title, fontsize = 20 )
    ax.set_xlabel(latex_xname[nome_x], fontsize = 20)
    ax.set_ylabel(latex_yname[nome_y][0], fontsize = 20)

    plt.grid(color='gray')
    plt.show(block = block_fig)





def mode_2(out_file: str) -> tp.NoReturn:
    '''Function called from the alternative interactive mode. Plots the results of a previous simulation'''

    datas = salva.read_data(out_file)
    
    if not datas['d_oss']:
        #Raise if no observable found in file
        raise IndexError
    
    msg = 'Default temperature unit: {}. Change into {}? (Y/N) [default: N]\n'.format(datas['unitx'], datas['unitx']=='beta' and 'T' or 'beta')
    temp = sml.user_while(msg, df = 'n')
    
    #Sets units and scale 
    datas['unitx'] , g = temp and (datas['unitx']=='beta' and 'T' or 'beta', (lambda x: 1/x))  or  (datas['unitx'], (lambda x: x))
    datas['x_axis'] = [g(x) for x in datas['x_axis'] ]

    #Plots a graph for every observable in saved file
    for oss in datas['d_oss']:
        block = oss == list(datas['d_oss'])[-1]
        plot_graph(datas['x_axis'], datas['d_oss'][oss]['valore'], datas['d_oss'][oss]['errore'], datas['L'] , datas['extfield'], datas['unitx'], oss, block_fig = block)



"""

def mode_3():
    os.chdir('./MC_stories')
    print('Ci sono queste storie: ')
    for dir in os.listdir():
        if dir.startswith('L='):
            print(dir)
    gen_oss = input('Calculate L=')
    os.chdir('L=' + gen_oss)
    ran = []
    dich = {}
    for MC_s in os.listdir():
        s = MC_s.rstrip('.txt').replace(',','.').split('_')
        #print(s)
        if s[0].lstrip('h') not in dich.keys():
            dich[s[0].lstrip('h')] = []
        dich[s[0].lstrip('h')].append(float(s[1].lstrip('beta')))
    
    print((f"In L={gen_oss} you have the following stories:\n"))
    fmt = ('extfield = {}, beta = [{}, {}] with {} points')
    for key in dich.keys():
        print(fmt.format(key, min(dich[key]), max(dich[key]), len(dich[key])))
    
    try_h = input('Choose the extfield value:\n').strip()
    #try_h = try_h in dich.keys() and try_h or None
    while try_h not in dich.keys():
        try_h = input('Insert extfield between {}'.format(', '.join(dich.keys()))).strip()
    print(dich)



while True:
        temp = input().lower().strip()
        if temp in ['y','','n'] :
            break
        else:
            print('Not understood, try again.')
"""