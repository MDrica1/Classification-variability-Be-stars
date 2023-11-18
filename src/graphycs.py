import numpy as np
import matplotlib.pyplot as plt
import pyhdust.spectools as pst
import requests as _requests
import astropy.io.fits as _pyfits
import pandas as pd
import wget as _wget
import xmltodict as _xmltodict
from PyAstronomy import pyasl

df = pd.read_csv("tabela-F.csv")

obs = df['Nº de observações'].values
F = df['$F$'].values
m = df['Ajuste ($dot{EW}\,(\AA/\mathrm{ano})$ )'].values
EWmedio = df['$\overline{EW} (\AA)$'].values
tempo_anos = df['Período observado (anos)'].values
Var = df['Var EW ($\AA$)'].values
QualAjs = df['Qualidade do ajuste (\%)'].values
tipoB = df['Tipo B'].values
tipoA = df['Tipo A'].values
tipoO = df['Tipo O'].values
vseni = df['Vseni ($Km/s$)'].values


# transforming data
def transform_data(src):
    new_data=[]
    d = [not pd.isnull(n) for n in src]
    a = src[d]
    for i in a:
        i = float(i.replace(',','.'))
    new_data.append(i)
    new_data = np.array(new_data)
    return new_data

F = transform_data(F)
m = transform_data(m)
EWmedio = transform_data(EWmedio)
obs = transform_data(obs)
tempo_anos = transform_data(tempo_anos)
Var = transform_data(Var)
QualAjs =transform_data(QualAjs)
tipoB = transform_data(tipoB)
tipoA = transform_data(tipoA)
tipoO = transform_data(tipoO)
vseni = transform_data(vseni)


#Graphics

plt.figure()
#plt.title('F')
plt.xlabel('F')
plt.ylabel('Número de objetos')
#plt.xlim(-2000,30000)
h = plt.hist(F, bins=5000) 


plt.figure()
#plt.title('Quantidade de espectros')
plt.xlabel('Número de Espectros')
plt.ylabel('Número de objetos')
plt.xlim(0,1780)
h = plt.hist(obs, bins=200) 


plt.figure()
plt.xlabel('Taxa de variação ($\dot{EW}\,(\AA)$')
plt.ylabel('Número de objetos')
#plt.xlim(-0.02,0.02)
h = plt.hist(m, bins=10000) 

plt.figure()
#plt.title('Período de observação')
plt.xlabel('Tempo de observação (anos)')
plt.ylabel('Número de objetos')
plt.ylim(0,31)
h = plt.hist(tempo_anos, bins=1000) 


plt.figure()
#plt.title('Período de observação')
plt.xlabel('$\overline{EW} (\AA)$)')
plt.ylabel('Número de objetos')
plt.ylim(-70,20)
h = plt.hist(EWmedio, bins=1000) 

plt.figure()
plt.title('Qualidade do Ajuste Linear (%)')
plt.xlabel('Erro de m')
plt.ylabel('')
plt.xlim()
h = plt.hist(QualAjs, bins=50) 

'''
plt.figure()
plt.title('Tipo espectral')
plt.xlabel('')
plt.ylabel('')
plt.xlim()

h = plt.hist(Bnovo, bins=50, label='Tipo B')

h = plt.hist(Anovo, bins=50, label='Tipo A')

h = plt.hist(Onovo, bins=50, color='red',label='Tipo O')
plt.legend()
'''

plt.figure()
plt.title('Distribuição de velocidades')
plt.xlabel('Vseni(Km/s)')
plt.ylabel('Número de objetos')
plt.xlim()

h = plt.hist(vseni, bins=50) 

#Vseni x Desvio padrão(EW) 

std = np.sqrt(Var)

plt.figure()
plt.title( 'Vseni X Desvio Padrão de EW')
plt.ylabel('Desvio Padrão de EW ($\AA$)')
plt.xlabel('Velocidade de rotação (Km/s)')
#plt.xlim(0,1780)
plt.plot(vseni,std)


