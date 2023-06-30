import matplotlib.pyplot as plt
import os
import numpy as np

mod = "PID"         #valori possibili OnOff oppure PID
V_onoff = 0        #settare tutti i valori relativi all' esperimento di cui si vuole fare il grafico
Kp = 0
Ki = 0
Kd = 0
t_setpoint = 80
num = 22                #numero dell' esperimento (serve per )
temperatura = []
tempo = []
colore_grafico = ""    #colore del grafico
directory_dati = r""    #inserire la propria directory dove vengono posti i dati ricavati dagli esperimenti
percorso_file_descrizioni = r""  #inserire il percorso al file di descrizioni
directory_grafici = r""    #inserire percorso della directory dei grafici

for file in os.listdir(directory_dati):
    if(file == "temperatura.txt"):
        with open(os.path.join(directory_dati,"temperatura.txt"),'r') as file:
            for riga in file:
                temperatura.append(float(riga[:len(riga)-1]))    #toglie gli \n alla fine della riga
        os.rename(os.path.join(directory_dati,"temperatura.txt"),os.path.join(directory_dati,"temperatura_"+str(num)+".txt"))    #rinomina il file temperatura (quello uscito dall' esperimento)
                                                                                                                                #in uno contraddistinto da un numero legato allo specifico esperimento
    if(file == "tempo.txt"):
        with open(os.path.join(directory_dati,"tempo.txt"),'r') as file:
            for riga in file:
                tempo.append(float(riga[:len(riga)-1]))
        os.rename(os.path.join(directory_dati,"tempo.txt"),os.path.join(directory_dati,"tempo_"+str(num)+".txt"))

fig, ax = plt.subplots()
ax.plot(tempo,temperatura,color=colore_grafico)
ax.axhline(y=t_setpoint, linestyle='dotted', color='black')
plt.yticks(np.linspace(30, 100, 8))
ax.set_title("Modalità " + mod)
if(mod == "OnOff"):
    annotazione = "V_on: "+ str(V_onoff)
elif(mod == "PID"):
    annotazione = "Kp: " + str(Kp) + "\nKi: " + str(Ki) + "\nKd: " + str(Kd) 
plt.annotate("Parametri:\n\n" + annotazione, xy=(max(tempo)-30, 100), xycoords='data',
             xytext=(-10, -10), textcoords='offset points',
             ha='left', va='top',bbox=dict(boxstyle='square', fc='white', ec='black'))
annotazione = annotazione.replace("\n","\t")
with open(percorso_file_descrizioni, "a") as file:
    file.write(str(num) + ") " + mod + "\t" + annotazione + "\n")
plt.savefig(os.path.join(directory_grafici,"graph_{}".format(num)))
