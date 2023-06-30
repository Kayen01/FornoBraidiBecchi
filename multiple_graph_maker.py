import numpy as np
import matplotlib.pyplot as plt
import os

numeri_esperimenti_da_graficare = []    #inserire i numeri relativi ai grafici da porre in un unico grafico
labels = []                            #riempire con tanti zeri quanti è len(numeri_esperimenti_da_graficare)
colors = ["red","blue","orange","green","brown"]    #inserire tanti colori quanti sono gli esperimenti da graficare
inizio_taglio_stringa = 25                            #le label dei grafici vengono estratte dal file descrizioni, questo indica da dove partire in ogni riga per prendere solo il dato che ci interessa
nomegrafico = "Kd_Tutti.png"
ncol_legenda = 3

directory_elettronica = r""     #directory generale dell'esperimento

#riempimento labels
for i in numeri_esperimenti_da_graficare:
    with open(os.path.join(directory_elettronica,"Descrizioni.txt"),"r") as descrizioni:
        for riga in descrizioni:
            if(riga.startswith(str(i)+")")):
                labels[numeri_esperimenti_da_graficare.index(i)] = riga[inizio_taglio_stringa:].replace("\t","").replace("\n","")    #inserire un numero -n dopo i due punti se necessario

fig,ax = plt.subplots()
for i in range(len(numeri_esperimenti_da_graficare)):
    temperatura = []
    tempo = []
    with open(os.path.join(directory_elettronica,r"Dati\\temperatura_{}.txt".format(numeri_esperimenti_da_graficare[i])),"r") as filetemperatura:
        for riga in filetemperatura:
                temperatura.append(float(riga[:len(riga)-1]))
    with open(os.path.join(directory_elettronica,r"Dati\\tempo_{}.txt".format(numeri_esperimenti_da_graficare[i])),"r") as filetempo:
        for riga in filetempo:
                tempo.append(float(riga[:len(riga)-1]))
    ax.plot(tempo,temperatura,color=colors[i],label=labels[i])

ax.legend(ncol=ncol_legenda)
plt.ylabel("Temperatura (°C)")
plt.xlabel("Tempo (s)")
plt.savefig(os.path.join(directory_elettronica,"Grafici\\{}".format(nomegrafico)))
