"""""""""""""""""""""""""""""""""""
        ATIVIDADE PRÁTICA 2
"""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""
        PALETA DE CORES
"""""""""""""""""""""""""""""""""""
# AZUL ESCURO: #002845
# ROSA CLARO: #E898AC
# AZUL CLARO: #00CFCC
# LARANJA CLARO: #FF9973
# AMARELO PYTHON: #F8C63D

"""""""""""""""""""""""""""""""""
          IMPORTAÇÕES
"""""""""""""""""""""""""""""""""
import os
import numpy as np
import math as math
import pandas as pd

import wooldridge as woo
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
# import functions.colors as f_color

"""""""""""""""""""""""""""""""""""
            FUNÇÕES
"""""""""""""""""""""""""""""""""""
# PADRÕES DE CORES DOS GRÁFICOS
def setChartDefaultColors(color):
    plt.rcParams['axes.edgecolor'] = color
    plt.rcParams['axes.labelcolor'] = color
    plt.rcParams['xtick.color'] = color
    plt.rcParams['ytick.color'] = color


"""""""""""""""""""""""""""""""""
       PROGRAMA PRINCIPAL
"""""""""""""""""""""""""""""""""

# DEFINIR AS CORES DE FUNDO DOS GRÁFICOS
setChartDefaultColors('white')

# DEFININDO CAMINHO DO PROJETO
os.chdir('B:\\Programing\\python\\ufsj\\econometria\\atividades\\atividade-pratica-ii\\data')
os.getcwd()

# IMPORTANDO A BASE DE DADOS
# - cumgpa: ponto cumulativo da faculdade
# - sat: pontuação SAT
# - hsperc: porcentagem de classificação do ensino médio
# - tothrs: total de horas em cursos universitários
bd3 = woo.dataWoo("gpa3")

"### 1 - ESTIMAR O MODELO USANDO MQO"
reg = smf.ols(formula='cumgpa ~ sat + hsperc + tothrs', data=bd3)
res = reg.fit() # resultados
usq = res.resid ** 2 # resíduos da regressão ao quadrado: ui^2


"### 2 - IMPRIMINDO E ANALISANDO OS RESULTADOS"
print(res.summary())


"### 3 - ANALISANDO O GRÁFICO DOS RESÍDUOS"
# Plotar o gráfico
bd3['u'] = res.resid
bd3['u_d1'] = res.resid.shift(1)
reg_fig = plt.scatter(x=bd3['u'], y=bd3['u_d1'], s=10, marker='o', facecolor='#00cfcc')

# Adicionando textos no gráfico
reg_fig = plt.ylabel('Resíduos', color='white')
reg_fig = plt.xlabel('Observações', color='white')
reg_fig = plt.title('Gráfico 1 - Resíduos da regressão', color='white')

# Salvar imagem e mostrar
reg_fig = plt.savefig("images\\01-residuos.png", transparent=True)
reg_fig = plt.show()


"### 4 - CALCULANDO O FATOR DE INFLAÇÃO DA VARIÂNCIA"
# sat = f(hsperc, tothrs)
reg_sat = smf.ols(formula='sat ~ hsperc + tothrs', data=bd3)
res_sat = reg_sat.fit()
usq_sat = res_sat.resid ** 2
fiv = 1 / (1 - res_sat.rsquared)
print(f"{fiv:.3f}") # 1.188

# hsperc = f(sat, tothrs)
reg_hsperc = smf.ols(formula='hsperc ~ sat + tothrs', data=bd3)
res_hsperc = reg_hsperc.fit()
usq_hsperc = res_hsperc.resid ** 2
fiv = 1 / (1 - res_hsperc.rsquared)
print(f"{fiv:.3f}") # 1.179

# tothrs = f(sat, hsperc)
reg_tothrs = smf.ols(formula='tothrs ~ sat + hsperc', data=bd3)
res_tothrs = reg_tothrs.fit()
usq_tothrs = res_tothrs.resid ** 2
fiv = 1 / (1 - res_tothrs.rsquared)
print(f"{fiv:.3f}") # 1.040


"### 5 - CALCULANDO O ERRO PADRÃO ROBUSTO"
# Calculando manualmente

# sat = f(hsperc, tothrs)
varusq = usq_sat * usq
varnum = sum(varusq)
varden = (sum(usq_sat)) ** 2
var_sat = (varnum/varden)
ep_sat = math.sqrt(var_sat)
t_sat = (res.params[1]) / ep_sat

# hsperc = f(sat, tothrs)
varusq = usq_hsperc * usq
varnum = sum(varusq)
varden = (sum(usq_hsperc)) ** 2
var_hsperc = (varnum/varden)
ep_hsperc = math.sqrt(var_hsperc)
t_hsperc = (res.params[2]) / ep_hsperc

# tothrs = f(sat, hsperc)
varusq = usq_tothrs * usq
varnum = sum(varusq)
varden = (sum(usq_tothrs)) ** 2
var_tothrs = (varnum/varden)
ep_tothrs = math.sqrt(var_tothrs)
t_tothrs = (res.params[3]) / ep_tothrs

# interc = f(sat, hsperc, tothrs)
bd3['interc'] = 1
reg_interc = smf.ols(formula='interc ~ 0 + sat + hsperc + tothrs', data=bd3)
res_interc = reg_interc.fit()
usq_interc = res_interc.resid ** 2
varusq = usq_interc * usq
varnum = sum(varusq)
varden = (sum(usq_interc)) ** 2
var_interc = (varnum/varden)
ep_interc = math.sqrt(var_interc)
t_interc = (res.params[0]) / ep_interc

varexp = np.array(['intercept', 'sat', 'hsperc', 'tothrs'])
beta   = np.array([res.params[0], res.params[1], res.params[2], res.params[3]])
ep_rob = np.array([ep_interc, ep_sat, ep_hsperc, ep_tothrs])
t_rob  = np.array([t_interc, t_sat, t_hsperc, t_tothrs])

res_rob = pd.DataFrame({'b': beta, 'ep_rob': ep_rob, 't_rob': t_rob})
res_robust = round(res_rob.set_index(varexp), 4)
res_robust.to_excel('tables/erros-robustos-manual.xlsx')
print(f"res_robust: {res_robust}")

# Calculando pela Matriz de Covariâncias: HCO
reg_cumgpa = smf.ols(formula='cumgpa ~ sat + hsperc + tothrs', data=bd3)
res_cumgpa = reg_cumgpa.fit(cov_type='HC0')
table_results = pd.DataFrame({
    'b': round(res_cumgpa.params, 4),
    'se': round(res_cumgpa.bse, 4),
    't': round(res_cumgpa.tvalues, 4),
    'pval': round(res_cumgpa.pvalues, 4)
})
table_results.to_excel('tables/erros-robustos-hco.xlsx')
print(f"table_results: {table_results}")


"### 6. TESTE DE AUTOCORRELAÇÃO BRESCH-GODFREY (BG)"
# bg_result = sm.stats.diagnostic.acorr_breusch_godfrey(res, nlags=3)
# fstat_auto = bg_result[2]
# fpval_auto = bg_result[3]
# print(f'fstat_auto: {fstat_auto:.4f}\n') # 0,5126
# print(f'fpval_auto: {fpval_auto:.4f}\n') # 0,6737

bd3['resid'] = res.resid
bd3['resid_lag1'] = bd3['resid'].shift(1)
bd3['resid_lag2'] = bd3['resid'].shift(2)
bd3['resid_lag3'] = bd3['resid'].shift(3)

reg_manual = smf.ols(formula='resid ~ resid_lag1 + resid_lag2 + resid_lag3 + sat + hsperc + tothrs', data=bd3)
res_manual = reg_manual.fit()

hypotheses = ['resid_lag1 = 0', 'resid_lag2 = 0', 'resid_lag3 = 0']
ftest_manual = res_manual.f_test(hypotheses)
fstat_manual = ftest_manual.statistic
fpval_manual = ftest_manual.pvalue
print(f'fstat_manual: {fstat_manual:.4f}\n') # 0,5140
print(f'fpval_manual: {fpval_manual:.4f}\n') # 0,6727


"### 7 - ESTIMANDO PELA MATRIZ DE COVARIÂNCIA HAC"

res_hac = reg.fit(cov_type='HAC', cov_kwds={'maxlags': 1})
tab_hac = pd.DataFrame({
    'b': round(res_hac.params, 4),
    'se': round(res_hac.bse, 4),
    't': round(res_hac.tvalues, 4),
    'pval': round(res_hac.pvalues, 4)
})

print(res_hac.summary())

tab_hac.to_excel('tables/tabela-hac.xlsx')
print(f'\n tabela_hac: \n{tab_hac}\n')

# Plotar o gráfico
reg_fig = plt.scatter(x=res.resid, y=res.resid.shfit(1), s=10, marker='o', facecolor='#00cfcc')
# reg_fig = plt.scatter(x=bd3['cumgpa'], y=res.resid, s=10, marker='o', color='#F8C63D')

# Adicionando textos no gráfico
reg_fig = plt.ylabel('Resíduos', color='white')
reg_fig = plt.xlabel('Observações', color='white')
reg_fig = plt.title('Gráfico 2 - Resíduos da regressão', color='white')

# Salvar imagem e mostrar
reg_fig = plt.savefig("images\\02-residuos.png", transparent=True)
reg_fig = plt.show()



"### 8 - MODELO ESTIMADO POR MQGF"
# d = 2
# d = 2(1-ro)
# ro = 1-d/2

rodw=1-(2/2)
print(f'\nRÔ = {rodw}\n')

# Transformando as variáveis para estimar o MQG
bd3['cumgpa_lag'] = bd3['cumgpa'].shift(1)
bd3['sat_lag'] = bd3['sat'].shift(1)
bd3['hsperc_lag'] = bd3['hsperc'].shift(1)
bd3['tothrs_lag'] = bd3['tothrs'].shift(1)

bd3['cumgpa_ro'] = bd3['cumgpa']-bd3['cumgpa_lag']*rodw
bd3['sat_ro'] = bd3['sat']-bd3['sat_lag']*rodw
bd3['hsperc_ro'] = bd3['hsperc']-bd3['hsperc_lag']*rodw
bd3['tothrs_ro'] = bd3['tothrs']-bd3['tothrs_lag']*rodw

reg_mqgf = smf.ols(formula='cumgpa_ro ~ sat_ro + hsperc_ro + tothrs_ro',data=bd3)
res_mqgf = reg_mqgf.fit()
print(res_mqgf.summary())


"### 9 - INTERPRETAÇÃO DOS COEFICIENTES"
