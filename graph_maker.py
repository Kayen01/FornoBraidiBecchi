import matplotlib.pyplot as plt
import os
import numpy as np

mod = "PID"         #valori possibili OnOff oppure PID
V_onoff = 5
Kp = 0.1
Ki = 0.011
Kd = 0.07
t_setpoint = 80
num = 22
temperatura = []
tempo = []
colore_grafico = "brown"
directory_dati = r"C:\\Users\\feder\\OneDrive\\Desktop\\Roba\\Scuola\\Università\\Elettronica e Acquisiszione Dati\\Dati"

for file in os.listdir(directory_dati):
    if(file == "temperatura.txt"):
        with open(os.path.join(directory_dati,"temperatura.txt"),'r') as file:
            for riga in file:
                temperatura.append(float(riga[:len(riga)-1]))
        os.rename(os.path.join(directory_dati,"temperatura.txt"),os.path.join(directory_dati,"temperatura_"+str(num)+".txt"))
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
with open(r"C:\\Users\\feder\\OneDrive\\Desktop\\Roba\\Scuola\\Università\\Elettronica e Acquisiszione Dati\\Descrizioni.txt", "a") as file:
    file.write(str(num) + ") " + mod + "\t" + annotazione + "\n")
plt.savefig(r"C:\\Users\\feder\\OneDrive\\Desktop\\Roba\\Scuola\\Università\\Elettronica e Acquisiszione Dati\\Grafici\\graph_{}".format(num))
