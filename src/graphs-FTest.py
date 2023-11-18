#!/usr/bin/env python3

import astropy.io.fits as pyfits
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import pandas as pd
from scipy.stats import f

#Normalizes
def normalizes(flux, length):
    left_edge = length < length.min() + 5
    right_edge = length > length.max() - 5
    f1 = np.median(flux[left_edge])
    f2 = np.median(flux[right_edge])
    comp1 = length[0]
    comp2 = length[-1]
    fc = f1 + ((f2-f1)/ (comp2-comp1))*(comp - comp1)
    f_norm = flux/fc
    return(f_norm) 

#EW calculation and sigmaEW estimation by the bootstrapping method
def sigma_emulation(norm_f,length):
    #Takes the length inside a box of 10 angstroms on each edge
    left = lenght < lenght.min() + 10
    right = lenght > lenght.max() - 10
    #Calculates the standard deviation of the normalized flux at the edges
    sigma = np.std(np.hstack([norm_f[left], norm_f[right]]))  
    a = sqrt(1+((norm_f)**2))
    sigma_t = sigma*a
    EWfake=[] #List to store the values emulated by the bootstrapping method.
    #Application of the Bootstrapping method. 
    for j in range(1000):
        ffake = norm_f + sigma_t*np.random.randn(len(norm_f)) #Emulates a flux based on the standard deviation calculated at the edges and along the entire length of the normalized flux.
        EWfake.append(np.trapz(1-ffake, x=length)) #ccalculates EW from emulated flux and adds each value to a list.
   
    sigmaEW=np.std(EWfake) #Standard deviation of emulated uncertainties
    sigmaEWlista.append(sigmaEW)
    
    return(sigmaEWlista) 

Flist = glob('*.fits')

EWlist = [] #Equivalent width
HJDlist = [] #Julian day with heliocentric correction
sigmaEWlist = []

fig, (ax1, ax2)=plt.subplots(2,1)

title_spectra = input("Title of you spectra:")
ax1.set_title(title_spectra)
ax1.set_xlabel('Comprimento de onda($\AA$)')
ax1.set_ylabel('Fluxo normalizado') 

#selection of region of interest
comp0 = 6562.8 #wavelength of H-alpha
comp1 = 6519.0 
comp2 = 6606.5


for i in Flist:
 fits = pyfits.open(i)
 dados = fits[1].data
 comp = dados['WAVE']
 fluxo = dados['FLUX']
 HJD = float(fits[0].header['MID-HJD'])
 keep = (comp >= comp1) * (comp <= comp2) #Cut spectra within a range
 comp = comp[keep]
 fluxo = fluxo[keep]
 keep = (comp > 6560) * (comp < 6565)
 
 if keep.any(): #Only spectra containing the H-alpha region
     try:
        f_norm = normalizes(fluxo,comp)
        EWlist.append(np.trapz(1-f_norm, x=comp)) #calculates equivalent width of H-alpha
        sigmaEWlist = sigma_emulation(f_norm,comp)
     except:
         Flist.remove(i)
         continue
 else:

     Flist.remove(i)
     continue 

ax1.plot(comp, f_norm)  


  
HJDlist = np.array(HJDlist)
EWlist = np.array(EWlist)
sigmaEWlist = np.array(sigmaEWlist)

#Calculates F-values

s2 = np.var(EWlist) #temporal standard deviation
sigma_mean = np.mean(sigmaEWlist) #average measurement uncertainty, obtained by the bootstrapping method
sigma_jones = 0.03*EWlist

F = s2/(sigma_mean**2) #F-value
F_alternative = s2/(sigma_jones**2) #F-value using sigma obtained by the Jones (2011) method

#Calculation of p value and confidence level of the F statistic test
df1 = len(EWlist) - 1
df2 = df1
alpha = 0.05 

p_value = f.sf(F, df1, df2)

C = 1 - p_value

df1 = len(EWlist) - 1
df2 = df1
alpha = 0.05  
from scipy.stats import f
p_value = f.sf(F, df1, df2)

C = 1 - p_value
   
#Graph of the evolution of the Equivalent Width of H-alpha over observed time

EW_mean=np.mean(EWlist) # mean value of EW
sigma=np.sqrt(np.var(EWlist)) # sigma range from mean value
hdl = HJDlist - 2400000 #standard

ax2.set_xlabel('Julian Heliocentric Day - 2400000') 
ax2.set_ylabel('Wavelength($\AA$)')
ax2.axhline(EW_mean,ls='--', color='red') #horizontal line representing the average value of EW
ax2.axhline(EW_mean+sigma, color='red',ls='--')
ax2.axhline(EW_mean-sigma,color='red', ls='--')
ax2.errorbar(hdl,EWlist,yerr=sigmaEWlist, fmt='.')

#Makes a linear fit to indicate a trend of EW behavior on the graph
coef,cov=np.polyfit(hdl,EWlist,1,cov=True) 
ax2.plot(hdl,np.poly1d(coef)(hdl),color='black')
ax2.set_ylim(plt.ylim()[::-1]) 
#ax2.tight_layout(pad=0.3)

#values to be stored in a table

Obs = len(Flist) #Number of spectra containing the H-alpha region for the star
Period1 = min(hdl) #minimum observation date
Period2 = max(hdl) #maximum observation date


'''
    
def Preparatory_function(lista, file):
    fits = pyfits.open(file)
    dados = fits[1].data
    comp = dados['WAVE']
    flux = dados['FLUX']
    HJD = float(fits[0].header['MID-HJD'])
   
    #selection of region of interest
    comp0 = 6562.8 #wavelength of H-alpha
    comp1 = 6519.0 
    comp2 = 6606.5
    keep = (comp >= comp1) * (comp <= comp2) #Cut spectra within a range
    comp = comp[keep]
    flux = flux[keep]
    keep = (comp > 6560) * (comp < 6565) 
    if keep.any(): #Only spectra containing the H-alpha region
        try:
            f_norm = Normalizes(flux, comp)
            EWlist,sigmaEWlist = Sigma_emulation(f_norm)
            
            HJDlista.append(HJD)
            HJDlist = np.array(HJDlista)            
        except:
            lista.remove(file)
            continue
    else:
        lista.remove(file)
        continue 
    
    return(comp, f_norm, HJDlist, EWlist, sigmaEWlist)


for i in Flist:
    comp,f_norm, HJDlist, EWlist, sigmaEWlist = Preparatory_function(Flist, i)
     #Plots all superimposed star spectra
     #ax1.set_title('V442 And')
     ax1.set_xlabel('Wavelength($\AA$)')
     ax1.set_ylabel('Normalized flux') 
     ax1.plot(comp, f_norm)
     
'''