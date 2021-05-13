'''Plot function and mode 2 plotting'''

import matplotlib.pyplot as plt
from numpy.core.shape_base import block
from isinglib import salva
import typing as tp


def plot_graph(x: tp.List[float], y: tp.List[float], dy: tp.List[float], L: int , h: float, nome_x: str, nome_y: str) -> tp.NoReturn:
    '''Graph plotter with tex labels'''
    latex_xname = {'beta': '$\u03b2$', 'T': '$T$'}
    latex_yname = {'c': '$C$', 'chi': '$\chi$', 'ene': '$\epsilon$', 'binder': '$B$', 'mag': '$M$', 'amag': '$|M|$'}
    plt.errorbar(x, y, dy,  marker = '.')
    plt.title( 'L=%d, h=%.3f'%(L,h) )
    plt.xlabel(latex_xname[nome_x])
    plt.ylabel(latex_yname[nome_y])

    #Adjusting font
    plt.rc('font', size=12)          
    plt.rc('axes', titlesize=12)
    plt.rc('axes', labelsize=12)

    plt.grid()
    plt.show()


def mode_2(out_file: str) -> tp.NoReturn:
    '''Function called from the alternative interactive mode. Plots the results of a previous simulation'''
    datas=salva.read_data(out_file)

    while True:
        temp = input('Default temperature unit: {}. Change into {}? (Y/N) [default: N]\n'.format(datas['unitx'], datas['unitx']=='beta' and 'T' or 'beta')).lower().strip()
        if temp in ['y','','n'] :
            break
        else:
            print('Not understood, try again.')

    #Sets units and scale 
    datas['unitx'] , g = (temp in ['n','']) and (datas['unitx'], (lambda x: x)) or (datas['unitx']=='beta' and 'T' or 'beta', (lambda x: 1/x))
    datas['x_axis'] = [g(x) for x in datas['x_axis'] ]

    #Plots a graph for every observable in saved file
    for oss in datas['d_oss'].keys():
        plot_graph(datas['x_axis'], datas['d_oss'][oss]['valore'], datas['d_oss'][oss]['errore'], datas['L'] , datas['extfield'], datas['unitx'], oss)



