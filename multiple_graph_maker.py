import numpy as np
import matplotlib.pyplot as plt
import os

numeri_simulazioni_da_graficare = [18,19,20,21,22]
labels = [0,0,0,0,0]
colors = ["red","blue","orange","green","brown"]
inizio_taglio_stringa = 25
nomegrafico = "Kd_Tutti.png"
ncol_legenda = 3

directory_elettronica = r"C:\\Users\\feder\\OneDrive\\Desktop\\Roba\\Scuola\\Università\\Elettronica e Acquisiszione Dati"

#riempimento labels
for i in numeri_simulazioni_da_graficare:
    with open(os.path.join(directory_elettronica,"Descrizioni.txt"),"r") as descrizioni:
        for riga in descrizioni:
            if(riga.startswith(str(i)+")")):
                labels[numeri_simulazioni_da_graficare.index(i)] = riga[inizio_taglio_stringa:].replace("\t","").replace("\n","")

fig,ax = plt.subplots()
for i in range(len(numeri_simulazioni_da_graficare)):
    temperatura = []
    tempo = []
    with open(os.path.join(directory_elettronica,r"Dati\\temperatura_{}.txt".format(numeri_simulazioni_da_graficare[i])),"r") as filetemperatura:
        for riga in filetemperatura:
                temperatura.append(float(riga[:len(riga)-1]))
    with open(os.path.join(directory_elettronica,r"Dati\\tempo_{}.txt".format(numeri_simulazioni_da_graficare[i])),"r") as filetempo:
        for riga in filetempo:
                tempo.append(float(riga[:len(riga)-1]))
    ax.plot(tempo,temperatura,color=colors[i],label=labels[i])

ax.legend(ncol=ncol_legenda)
plt.savefig(os.path.join(directory_elettronica,"Grafici\\{}".format(nomegrafico)))