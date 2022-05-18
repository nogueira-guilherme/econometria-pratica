"""""""""""""""""""""""""""""""""""
        ATIVIDADE PRÁTICA 1
"""""""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""""
          IMPORTAÇÕES
"""""""""""""""""""""""""""""""""
import os
import numpy as np
import pandas as pd
import datetime as date
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

import Functions.Colors as color

"""""""""""""""""""""""""""""""""
       PROGRAMA PRINCIPAL
"""""""""""""""""""""""""""""""""

# SELECIONANDO DIRETÓRIO
os.chdir('D:\\Programing\\python\\econometria\\1-7-atividade-pratica\\Data')

# IMPORTANDO OS DADOS
df_estudantes = pd.read_excel("dados.xlsx")

# PADRÕES DE CORES DOS GRÁFICOS
plt.rcParams['axes.edgecolor'] = color
plt.rcParams['axes.labelcolor'] = color
plt.rcParams['xtick.color'] = color
plt.rcParams['ytick.color'] = color


# ESTATÍSTICAS
df_descricao = df_estudantes.describe()
df_descricao.to_excel('descricao.xlsx')
print(f"\n{df_descricao}\n")



'''
GRÁFICO DAS IDADES

Idade do estudante entrevistado (em anos)
'''
# Dados
df_idade = df_estudantes["idade"]
df_idade = pd.DataFrame(df_idade)
df_idade.columns = ['idade']

# Ordenar os valores e armazenar em objetos, para depois jogar em um DataFrame
ate_vinte = df_idade[(df_idade['idade']<=20)]
ate_vinte_cinco = df_idade[(df_idade['idade']>20)&(df_idade['idade']<=25)]
ate_trinta = df_idade[(df_idade['idade']>25)&(df_idade['idade']<=30)]
acima_trinta = df_idade[(df_idade['idade']>30)]

# Armazenando os dados em um objeto
frequencia_idade = {'Frequencia': [len(ate_vinte), len(ate_vinte_cinco), len(ate_trinta), len(acima_trinta)]}

# Guardar em um DataFrame
df_idade_frequencia = pd.DataFrame(frequencia_idade, index=['0', '1', '2', '3'])

# Plotar o gráfico
idade_x = ['Até 20 anos', '21 - 25 anos', '26 - 30 anos', 'Acima de 30 anos']
idade_y = df_idade_frequencia["Frequencia"]
idade_fig = idade_colors = ['#00cfcc', '#ff9973', '#e898ac', '#f8c63d']
idade_fig = plt.bar(idade_x, idade_y, color=idade_colors)

# Adicionando textos no gráfico
idade_fig = plt.ylabel('Número de estudantes', color='black')
idade_fig = plt.xlabel('Idade dos estudantes', color='black')
for cont in range(0, len(idade_y)):
    idade_fig = plt.text(cont, idade_y[cont], idade_y[cont], ha="center", va="bottom", color='black')

# Salvar imagem e mostrar
idade_fig = plt.savefig("Images\\idade.png", transparent=True)
idade_fig = plt.show()




'''
GRÁFICO DOS SEXOS

1 - Masculino
2 - Feminino
'''
# Dados
df_sexo = df_estudantes["sexo"].value_counts().sort_index()
df_sexo = pd.DataFrame(df_sexo)
df_sexo.columns = ['quantidade']

# Plotar o gráfico
sexo_x = df_sexo.quantidade
sexo_explode = (0, 0.1)
sexo_label = ['Masculino', 'Feminino']
sexo_colors = ['#00cfcc', '#e898ac']
sexo_fig = plt.pie(x=sexo_x, autopct='%.1f%%', explode=sexo_explode, shadow=True, colors=sexo_colors, textprops={'color': "w"}) # labels=sexo_label

# Adicionando textos no gráfico
sexo_fig = plt.title('Sexo dos Estudantes de Econometria 1', fontsize=18, color="black")

# Salvar imagem e mostrar
sexo_fig = plt.savefig("Images\\sexo.png", transparent=True)
sexo_fig = plt.show()




'''
GRÁFICO DOS TIMES

1 - Outro time
2 - Atlético MG
3 - Cruzeiro
4 - Nenhum time
'''
# Dados
df_time = df_estudantes["time"].value_counts().sort_index()
df_time = pd.DataFrame(df_time)
df_time.columns = ['quantidade']

# Plotar o gráfico
time_x = df_time.quantidade
time_label = ['Outro time', 'Atlético MG', 'Cruzeiro', 'Nenhum time']
time_colors = ['#FF9973', '#000000', '#00CFCC', '#e898ac']
time_fig = plt.pie(x=time_x, autopct='%.1f%%', labels=time_label, shadow=False, colors=time_colors, textprops={'color': "w"})

# Adicionando textos no gráfico
time_fig = plt.title('Time dos Estudantes de Econometria 1', fontsize=18, color="black")

# Salvar imagem e mostrar
time_fig = plt.savefig("Images\\time.png", transparent=True)
time_fig = plt.show()



'''
COMPUTADOR PESSOAL

0 - Não
1 - Sim
'''
# Dados
df_computador = df_estudantes["computador_pessoal"].value_counts().sort_index()
df_computador = pd.DataFrame(df_computador)
df_computador.columns = ['quantidade']

# Dados normalizados
pc_computador = round(df_estudantes["computador_pessoal"].value_counts(normalize=True).sort_index(), 4)
pc_computador = pd.DataFrame(pc_computador)
pc_computador.columns = ['porcentagem']

# Plotar o gráfico
computador_x = df_computador.quantidade
computador_y = ['Não', 'Sim']
computador_colors = ['#e898ac', '#00cfcc']
computador_fig = plt.barh(computador_y, computador_x, color=computador_colors)

# Adicionando textos no gráfico
computador_fig = plt.xlabel('Quantidade de estudantes', color='white')
computador_fig = plt.ylabel('O estudante possui computador pessoal?', color='white')
computador_fig = plt.annotate(f"{pc_computador.quantidade[0]*100:.2f}%", xy=(2,'Não'), ha="left", va="center", color='white')
computador_fig = plt.annotate(f"{pc_computador.quantidade[1]*100:.2f}%", xy=(31,'Sim'), ha="right", va="center", color='white')

# Salvar imagem e mostrar
computador_fig = plt.savefig("Images\\computador_pessoal.png", transparent=True)
computador_fig = plt.show()



'''
NÚMERO DE REPROVAÇÕES

'''
# Dados
df_reprovacao = df_estudantes["reprovacao"]
df_reprovacao = pd.DataFrame(df_reprovacao)
df_reprovacao.columns = ['quantidade']

# Plotar o gráfico
reprovacao_x = list(range(0, len(df_reprovacao), 1))
reprovacao_y = df_reprovacao.quantidade
reprovacao_fig = plt.scatter(reprovacao_x, reprovacao_y, marker='o', color='#00cfcc')

# Adicionando textos no gráfico
reprovacao_fig = plt.ylabel('Número de reprovações', color='white')
reprovacao_fig = plt.xlabel('Identificação do estudante', color='white')

# Salvar imagem e mostrar
reprovacao_fig = plt.savefig("Images\\reprovacao.png", transparent=True)
reprovacao_fig = plt.show()



'''
SATISFAÇÃO DO CURSO 

1 - Muito bom
2 - Bom
3 - Médio
4 - Muito baixo
'''
# Dados
df_satisfacao = df_estudantes["satisfacao_curso"].value_counts().sort_index()
df_satisfacao = pd.DataFrame(df_satisfacao)
df_satisfacao.columns = ['classificacao']

# Dados normalizados
pc_satisfacao = df_estudantes["satisfacao_curso"].value_counts(normalize=True).sort_index()
pc_satisfacao = pd.DataFrame(pc_satisfacao)
pc_satisfacao.columns = ['porcentagem']

# Plotar o gráfico
satisfacao_x = ['Muito bom', 'Bom', 'Médio', 'Muito baixo']
satisfacao_y = df_satisfacao.classificacao
satisfacao_yp = round(pc_satisfacao.porcentagem * 100, 2)
satisfacao_fig = satisfacao_colors = ['#f8c63d', '#00cfcc', '#ff9973', '#e898ac']
satisfacao_fig = plt.bar(satisfacao_x, satisfacao_y, color=satisfacao_colors)

# Adicionando textos no gráfico
satisfacao_fig = plt.ylabel('Número de estudantes', color='white')
satisfacao_fig = plt.xlabel('Grau de satisfação com o curso', color='white')
for cont in range(0, len(satisfacao_y)):
    satisfacao_fig = plt.text(cont, satisfacao_y[cont+1], f"{satisfacao_yp[cont+1]:.2f}%", ha="center", va="bottom", color='white')

# Salvar imagem e mostrar
satisfacao_fig = plt.savefig("Images\\satisfacao.png", transparent=True)
satisfacao_fig = plt.show()



'''
SATISFAÇÃO DO CURSO 

1 - Muito bom
2 - Bom
3 - Médio
4 - Muito baixo
'''
# Dados
df_expectativa = df_estudantes["expectativa_econometria"].value_counts().sort_index()
df_expectativa = pd.DataFrame(df_expectativa)
df_expectativa.columns = ['classificacao']
df_expectativa.loc[4] = [0] # como ninguém avaliou muito baixo, vou adicionar para aparecer 0

# Dados normalizados
pc_expectativa = df_estudantes["expectativa_econometria"].value_counts(normalize=True).sort_index()
pc_expectativa = pd.DataFrame(pc_expectativa)
pc_expectativa.columns = ['porcentagem']
pc_expectativa.loc[4] = [0]

# Plotar o gráfico
expectativa_x = ['Muito bom', 'Bom', 'Médio', 'Muito baixo']
expectativa_yp = round(pc_expectativa.porcentagem * 100, 2)
expectativa_y = df_expectativa.classificacao
expectativa_fig = expectativa_colors = ['#f8c63d', '#00cfcc', '#ff9973', '#e898ac']
expectativa_fig = plt.bar(expectativa_x, expectativa_y, color=expectativa_colors)

# Adicionando textos no gráfico
expectativa_fig = plt.ylabel('Número de estudantes', color='white')
expectativa_fig = plt.xlabel('Grau de expectativa em econometria', color='white')
for cont in range(0, len(expectativa_y)):
    expectativa_fig = plt.text(cont, expectativa_y[cont+1], f"{expectativa_yp[cont+1]:.2f}%", ha="center", va="bottom", color='white')

# Salvar imagem e mostrar
expectativa_fig = plt.savefig("Images\\expectativa.png", transparent=True)
expectativa_fig = plt.show()



'''
TEMPO EM REDES 

Número de horas gastas em redes sociais
'''
# Dados
df_tempo_redes = df_estudantes["tempo_redes"].value_counts().sort_index()
df_tempo_redes = pd.DataFrame(df_tempo_redes)
df_tempo_redes.columns = ['quantidade']

# Dados normalizados
pc_tempo_redes = round(df_estudantes["tempo_redes"].value_counts(normalize=True).sort_index(), 4)
pc_tempo_redes = pd.DataFrame(pc_tempo_redes)
pc_tempo_redes.columns = ['porcentagem']

# Plotar o gráfico
tempo_redes_x = df_tempo_redes["quantidade"]
tempo_redes_y = ['1.0', '1.5', '2.0','3.0', '4.0',  '8.0', '9.0']
tempo_redes_fig = plt.barh(tempo_redes_y, tempo_redes_x, color='#00cfcc')

# Adicionando textos no gráfico
tempo_redes_fig = plt.xlabel('Número de estudantes', color='white')
tempo_redes_fig = plt.ylabel('Horas gastas nas redes sociais', color='white')
for cont in range(0, len(tempo_redes_y)):
    posicao = 0
    if cont == 0:   posicao = 1.0
    elif cont == 1: posicao = 1.5
    elif cont == 2: posicao = 2.0
    elif cont == 3: posicao = 3.0
    elif cont == 4: posicao = 4.0
    elif cont == 5: posicao = 8.0
    elif cont == 6: posicao = 9.0
    tempo_redes_fig = plt.annotate(f"{tempo_redes_x[posicao]:.1f}%", xy=(tempo_redes_x[posicao], tempo_redes_y[cont]), ha="right", va="center", color='white')

# Salvar imagem e mostrar
tempo_redes_fig = plt.savefig("Images\\tempo_redes.png", transparent=True)
tempo_redes_fig = plt.show()



'''
NOTAS NO ENEM

Nota obtida no ENEM
'''
# Dados
df_enem = df_estudantes["enem"]
df_enem = pd.DataFrame(df_enem)
df_enem.columns = ['nota']

# Plotar o gráfico
enem_x = list(range(0, len(df_enem), 1))
enem_y = df_enem.nota
enem_fig = plt.scatter(enem_x, enem_y, marker='o', color='#00cfcc')

# Adicionando textos no gráfico
enem_fig = plt.ylabel('Nota no ENEM', color='white')
enem_fig = plt.xlabel('Identificação do estudante', color='white')

# Salvar imagem e mostrar
computador_fig = plt.savefig("Images\\enem.png", transparent=True)
enem_fig = plt.show()



'''
RELAÇÃO DO TEMPO GASTO EM REDES SOCIAIS 

'''

'''
a) De forma intuitiva, há de se esperar de que pessoas mais jovens tenham um maior contato com smartphones. 
Isso porque, é uma tecnologia historicamente recente, atraindo mais os jovens.   
Assim, em certo nível, quanto menor a idade, maior o tempo gasto em redes sociais. E quanto maior a idade, menor o tempo gasto em redes sociais.
'''


'''
Gráfico:

Identificação do aluno (x) X Nota Enem (y)
'''
# Dados
data_estudantes = df_estudantes[["idade","tempo_redes"]]
data_estudantes = df_estudantes

# Estimando a regressão
regressao = smf.ols(formula='np.log(tempo_redes) ~ idade', data=df_estudantes)

# Estimativas da regressão
results = regressao.fit()

# Tabela geral de resultados
print(results.summary())

print(results.fittedvalues)

# Plotar o gráfico
regressao_x = data_estudantes.idade
regressao_y = np.log(data_estudantes.tempo_redes) # results.fittedvalues
regressao_fig = plt.plot('idade', 'tempo_redes', data=data_estudantes, color='#00cfcc', marker='o', linestyle='')
regressao_fig = plt.plot(regressao_x, regressao_y, color='#ff9973', linestyle='-')

# Adicionando textos no gráfico
regressao_fig = plt.ylabel('Tempo gasto nas redes sociais', color='black')
regressao_fig = plt.xlabel('Idade dos estudantes', color='black')
regressao_fig = plt.title('ln(tempo_redes) = 1,8109 − 0,0362X', color='black')

# Salvar imagem e mostrar
regressao_fig = plt.savefig("Images\\regressao_teste.png", transparent=True)
regressao_fig = plt.show()

# Alfa = 1,8109
# Beta = -0.0362 = 3,62%
# P > |t| = 0,000

# Rejeitamos H₀ com mais de 99% de chance, ou seja, o estimador é estatisticamente diferente de zero.
# A cada 1 ano aumentado na idade dos estudantes, diminui-se em 3,62% o tempo gasto em redes sociais.










