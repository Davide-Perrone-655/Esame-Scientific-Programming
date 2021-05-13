import matplotlib.pyplot as plt
from isinglib import errors
from isinglib import salva


def plot_graph(x, y, dy, L , h, nome_x, nome_y):
    latex_xname = {'beta': '$\u03b2$', 'T': '$T$'}
    latex_yname = {'c': '$C$', 'chi': '$\chi$', 'ene': '$\epsilon$', 'binder': '$B$', 'mag': '$M$', 'amag': '$|M|$'}
    plt.errorbar(x, y, dy,  marker = '.')
    plt.title( 'L=%d, h=%.3f'%(L,h) )
    plt.xlabel(latex_xname[nome_x])
    plt.ylabel(latex_yname[nome_y])
    plt.grid()
    plt.show()

def mode_2(out_file):
    datas=salva.read_data(out_file)
    while True:
        temp = input('Default temperature unit: {}. Change into {}? (Y/N) [default: N]\n'.format(datas['unitx'], datas['unitx']=='beta' and 'T' or 'beta')).lower().strip()
        if temp in ['y','','n'] :
            break
        else:
            print('Not understood, try again.')
    datas['unitx'] , g = (temp in ['n','']) and (datas['unitx'], (lambda x: x)) or (datas['unitx']=='beta' and 'T' or 'beta', (lambda x: 1/x))
    datas['x_axis'] = [g(x) for x in datas['x_axis'] ]
    for oss in datas['d_oss'].keys():
        plot_graph(datas['x_axis'], datas['d_oss'][oss]['valore'], datas['d_oss'][oss]['errore'], datas['L'] , datas['extfield'], datas['unitx'], oss)


'''prende in input l'asse x, l'asse y e l'incertezza su y della temperatura in unità unit_x = 'T' (oppure 'beta') e restituisce in output l'asse y con incertezza dy della quantità "nome".
    Se salva_file=True, salva su file i dati del grafico.
    Se plot=True, stampa il plot.
'''
