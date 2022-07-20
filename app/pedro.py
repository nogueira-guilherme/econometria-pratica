import math as math
import os
import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import wooldridge as woo
import statsmodels.formula.api as smf

os.chdir('SEU CAMINHO')

df = woo.dataWoo("gpa3")

### 1 - ESTIMAR O MODELO USANDO MQO
reg_mqo = smf.ols(formula='cumgpa ~ sat + hsperc + tothrs', data=df)
res_mqo = reg_mqo.fit()
usq_mqo = res_mqo.resid ** 2

### 2 - IMPRIMINDO E ANALISANDO OS RESULTADOS
print(res_mqo.summary())

### 3 - ANALISANDO O GRÁFICO DOS RESÍDUOS
plt.scatter(res_mqo.resid, res_mqo.resid.shift(1), s=10, marker='o', facecolor='green')
plt.ylabel('Y')
plt.xlabel('X')
plt.title('Gráfico 01')
plt.savefig("grafico1.png")
plt.show()

### 4 - CALCULANDO O FATOR DE INFLAÇÃO DA VARIÂNCIA
reg_1 = smf.ols(formula='sat ~ hsperc + tothrs', data=df)
res_1 = reg_1.fit()
usq_1 = res_1.resid ** 2
fiv = 1 / (1 - res_1.rsquared)
print(fiv)

reg_2 = smf.ols(formula='hsperc ~ sat + tothrs', data=df)
res_2 = reg_2.fit()
usq_2 = res_2.resid ** 2
fiv = 1 / (1 - res_2.rsquared)
print(fiv)

reg_3 = smf.ols(formula='tothrs ~ sat + hsperc', data=df)
res_3 = reg_3.fit()
usq_3 = res_3.resid ** 2
fiv = 1 / (1 - res_3.rsquared)
print(fiv)


### 5 - CALCULANDO O ERRO PADRÃO ROBUSTO
# Manual
varusq_1 = usq_1 * usq_mqo
varnum_1 = sum(varusq_1)
varden_1 = (sum(usq_1)) ** 2
var_sat = (varnum_1 / varden_1)
ep_sat = math.sqrt(var_sat)
t_sat = (res_mqo.params[1]) / ep_sat

varusq_2 = usq_2 * usq_mqo
varnum_2 = sum(varusq_2)
varden_2 = (sum(usq_2)) ** 2
var_hsperc = (varnum_2 / varden_2)
ep_hsperc = math.sqrt(var_hsperc)
t_hsperc = (res_mqo.params[2]) / ep_hsperc

varusq_3 = usq_3 * usq_mqo
varnum_3 = sum(varusq_3)
varden_3 = (sum(usq_3)) ** 2
var_tothrs = (varnum_3 / varden_3)
ep_tothrs = math.sqrt(var_tothrs)
t_tothrs = (res_mqo.params[3]) / ep_tothrs

df['interc'] = 1
reg_interc = smf.ols(formula='interc ~ 0 + sat + hsperc + tothrs', data=df)
res_interc = reg_interc.fit()
usq_interc = res_interc.resid ** 2
varusq_5 = usq_interc * usq_mqo
varnum_5 = sum(varusq_5)
varden_5 = (sum(usq_interc)) ** 2
var_interc = (varnum_5 / varden_5)
ep_interc = math.sqrt(var_interc)
t_interc = (res_mqo.params[0]) / ep_interc

varexp = np.array(['intercept', 'sat', 'hsperc', 'tothrs'])
b = np.array([res_mqo.params[0], res_mqo.params[1], res_mqo.params[2], res_mqo.params[3]])
ep_rob = np.array([ep_interc, ep_sat, ep_hsperc, ep_tothrs])
t_rob  = np.array([t_interc, t_sat, t_hsperc, t_tothrs])

res_rob = pd.DataFrame({'b': b, 'ep_rob': ep_rob, 't_rob': t_rob})
res_robust = round(res_rob.set_index(varexp), 4)
print(res_robust)

# Matriz de Covariâncias: HCO
reg_6 = smf.ols(formula='cumgpa ~ sat + hsperc + tothrs', data=df)
res_6 = reg_6.fit(cov_type='HC0')
table_results = pd.DataFrame({
    'b': round(res_6.params, 4),
    'se': round(res_6.bse, 4),
    't': round(res_6.tvalues, 4),
    'pval': round(res_6.pvalues, 4)
})
print(table_results)


### 6. TESTE DE AUTOCORRELAÇÃO BRESCH-GODFREY (BG)
df['resid'] = res_mqo.resid
df['resid_lag1'] = df['resid'].shift(1)
df['resid_lag2'] = df['resid'].shift(2)
df['resid_lag3'] = df['resid'].shift(3)

reg_manual = smf.ols(formula='resid ~ resid_lag1 + resid_lag2 + resid_lag3 + sat + hsperc + tothrs', data=df)
res_manual = reg_manual.fit()

hypotheses = ['resid_lag1 = 0', 'resid_lag2 = 0', 'resid_lag3 = 0']
ftest_manual = res_manual.f_test(hypotheses)
fstat_manual = ftest_manual.statistic
fpval_manual = ftest_manual.pvalue
print(f'fstat_manual: {fstat_manual:.4f}\n') # 0,5140
print(f'fpval_manual: {fpval_manual:.4f}\n') # 0,6727



### 7 - ESTIMANDO PELA MATRIZ DE COVARIÂNCIA HAC
res_hac = reg_mqo.fit(cov_type='HAC', cov_kwds={'maxlags': 1})
tab_hac = pd.DataFrame({
    'b': round(res_hac.params, 4),
    'se': round(res_hac.bse, 4),
    't': round(res_hac.tvalues, 4),
    'pval': round(res_hac.pvalues, 4)
})

print(res_hac.summary())
print(tab_hac)


plt.scatter(df['cumgpa'], res_mqo.resid, s=10, marker='o', color='green')
plt.title('Gráfico 02')
plt.savefig("grafico2.png")
plt.show()



### 8 - MODELO ESTIMADO POR MQGF
rodw=1-(2/2)
print(rodw)

df['cumgpalag'] = df['cumgpa'].shift(1)
df['satlag'] = df['sat'].shift(1)
df['hsperclag'] = df['hsperc'].shift(1)
df['tothrslag'] = df['tothrs'].shift(1)
df['cumgparo'] = df['cumgpa'] - df['cumgpalag'] * rodw
df['satro'] = df['sat'] - df['satlag'] * rodw
df['hspercro'] = df['hsperc'] - df['hsperclag'] * rodw
df['tothrsro'] = df['tothrs'] - df['tothrslag'] * rodw

reg_mqgf = smf.ols(formula='cumgparo ~ satro + hspercro + tothrsro', data=df)
res_mqgf = reg_mqgf.fit()
print(res_mqgf.summary())


# 9 - INTERPRETAÇÃO DOS COEFICIENTES
