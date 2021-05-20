#!/usr/bin/env python3

'''Plot function and mode 2 plotting'''

from isinglib import ising_files as salva
from isinglib import ising_small as sml
import matplotlib.pyplot as plt
import typing as tp


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

