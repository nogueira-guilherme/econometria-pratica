"""""""""""""""""""""""""""""""""""
        FUNÇÕES DE CORES
"""""""""""""""""""""""""""""""""""
# AZUL ESCURO: #002845
# ROSA CLARO: #E898AC
# AZUL CLARO: #00CFCC
# LARANJA CLARO: #FF9973
# AMARELO PYTHON: #F8C63D

"""""""""""""""""""""""""""""""""
          IMPORTAÇÕES
"""""""""""""""""""""""""""""""""
import matplotlib.pyplot as plt


"""""""""""""""""""""""""""""""""
       PROGRAMA PRINCIPAL
"""""""""""""""""""""""""""""""""

# PADRÕES DE CORES DOS GRÁFICOS
def setChartDefaultColors(color):
    plt.rcParams['axes.edgecolor'] = color
    plt.rcParams['axes.labelcolor'] = color
    plt.rcParams['xtick.color'] = color
    plt.rcParams['ytick.color'] = color
    print(f'Cor padrão definida: {color}')























