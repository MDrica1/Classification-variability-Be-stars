'''
Exemplo mudança de nomes no eixo x
Adapte para o seu caso específico
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# gerando dados falsos
#dados = np.random.randint(-1, high=12, size=100)
df=pd.read_csv('tabela-F.csv')

tipo=df['Tipo '].values
EW=df['$\overline{EW} (\AA)$'].values
obs=df['Nº de observações'].values
tempo=df['Período observado (anos)'].values
vseni=df['$v\sin i (Km/s)$'].values
des=df['S_EW'].values

Vseni = [not pd.isnull(n) for n in vseni]
Des=[not pd.isnull(n) for n in des]
Tipo = [not pd.isnull(n) for n in tipo]
ew=[not pd.isnull(n) for n in EW]
Obs = [not pd.isnull(n) for n in obs]
Tempo = [not pd.isnull(n) for n in tempo]

vsenil=[]
tipovl=[]
desl=[]
tipol=[]
obsl=[]
ewl=[]
tempol=[]

for i in des[Tipo]:
    i = float(i.replace(',','.'))
    desl.append(i)

for i in tipo[Tipo]:
    i = float(i)
    tipol.append(i)
for i in obs[Tipo]:
    i = float(i)
    obsl.append(i)
for i in EW[Tipo]:
    i = float(i.replace(',','.'))
    ewl.append(i)
for i in tempo[Tipo]:
    i = float(i.replace(',','.'))
    tempol.append(i)

# Graph type X vseni

Tipo=[not pd.isnull(n) for n in tipo]
VseniT=vseni[Tipo]
Vseni = [not pd.isnull(n) for n in VseniT]
vseniType=VseniT[Vseni]

tipov=tipo[Tipo]
tipovseni=tipov[Vseni]

# graphics

obsl=np.array(obsl)
tempol=np.array(tempol)

obsv=obsl[Vseni]
tempov=tempol[Vseni]

fig, ax = plt.subplots()

#type x stdEW
graf=ax.scatter(tipol,desl,s=obsl,c=tempol,alpha=0.5) 
ax.set_ylabel('$Desvio Padrão de \overline{EW}\,(\AA)$')
ax.set_ylim(plt.ylim(-1,16))

#type x vseni

#graf=ax.scatter(tipovseni,vesniType,s=obsv,c=tempov,alpha=0.5, cmap='Purples')
#ax.axhline(230, ls='--',color='black',label='$\overline{v\sin i}=230\,Km/s$')
#ax.legend()
#ax.set_ylabel('$vseni (Km/s)$')
#ax.set_ylim(plt.ylim(-20,500))

#type x EW mean

#graf = ax.scatter(tipol,ewl,c=tempol,s=obsl,alpha=0.5)
#ax.set_ylabel('$\overline{EW}\,(\AA)$')
#ax.set_ylim(plt.ylim(-72,18)[::-1])

fig.colorbar(graf,ax=ax)
ax.set_xlabel('Tipo espectral')

# x-values
xvalores = np.arange(-3, 16)

# x-labels
xlabels = ['07','O8','O9', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'A0','A1','A2','A5','A9','F0']

# change x-labels
ax.set_xticks(xvalores)
ax.set_xticklabels(xlabels)
#plt.show()
