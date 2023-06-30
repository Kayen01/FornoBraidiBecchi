#include "stdafx.h"
#include <iostream>
#include <NIDAQmx.h>
#include <windows.h>
#include <conio.h>
#include <fstream>
#include <string>

using namespace std;

double conversione_tensione_temperatura(double Vin_mV)
{
	double C0 = -0.125079;
	double C1 = 1.04063;
	double C2 = 1.69477e-3;
	double C3 = 9.57745e-6;
	return C0+C1*Vin_mV+C2*(Vin_mV*Vin_mV)+C3*(Vin_mV*Vin_mV*Vin_mV);
}

int main(void)
{

	//definizione oggetti TaskHandle
	TaskHandle hTaskHandleIn;
	DAQmxCreateTask("", &hTaskHandleIn);
	DAQmxCreateAIVoltageChan(hTaskHandleIn,"Dev1/ai0","", DAQmx_Val_Cfg_Default,0.0,0.1,DAQmx_Val_Volts,"");
	DAQmxStartTask(hTaskHandleIn);

	TaskHandle hTaskHandleOut;
	DAQmxCreateTask("", &hTaskHandleOut);
	DAQmxCreateAOVoltageChan(hTaskHandleOut,"Dev1/ao0","", -10.0,10.0,DAQmx_Val_Volts,NULL);
	DAQmxStartTask(hTaskHandleOut);

	//definizione variabili
	double t_setpoint;
	double t_misurata;
	int scelta_mod;
	double t_c;
	double t = 0;
	int flag_cambio_tc;
	float64 Vin;
	double Vout_onoff;
	double Vout_pid;
	double Kp;
	double Ki;
	double Kd;
	double Vp;
	double Vi;
	double Vd;
	double err_new;
	double err_old = 0;
	double sum = 0;
	bool troppo;
	bool sbagliato_mod;
	bool sbagliato_vout;
	bool sbagliato_tc;


	//interfaccia
	cout<<"Programma di controllo del forno"<<endl;

	//scelta t_setpoint
	do
	{
		troppo = false;
		cout<<"Fornire la temperatura da far raggiungere al forno (inferiore a 110 gradi Celsius)"<<endl;
		cin>>t_setpoint;
		if(t_setpoint>=110)
		{
			troppo = true;
			cout<<"Temperatura sopra alla soglia massima"<<endl;
		}
	}while(troppo);

	//scelta modalità di controllo
	do
	{
		sbagliato_mod = false;
		cout<<"Selezionare la modalità di controllo"<<endl;
		cout<<"1 --> On/Off"<<endl;
		cout<<"2 --> PID"<<endl;
		cin>>scelta_mod;
		if(scelta_mod!=1 && scelta_mod!=2)
		{
			sbagliato_mod = true;
			cout<<"Il valore inserito non è tra i valori permessi"<<endl;
		}
	}while(sbagliato_mod);

	if(scelta_mod==1)
	{
		do
		{
			sbagliato_vout = false;
			cout<<"Inserire il valore di V costante che viene applicato quando la temperatura del forno non  ha raggiunto quella di setpoint"<<endl;
			cin>>Vout_onoff;
			if(Vout_onoff<0)
			{
				sbagliato_vout = true;
				cout<<"Il valore di V non può essere inferiore a 0"<<endl;
			}
		}while(sbagliato_vout);
	}
	else
	{
		cout<<"Inserire i valori delle seguenti costanti:"<<endl;
		cout<<"Kp:"<<endl;
		cin>>Kp;
		cout<<"Ki:"<<endl;
		cin>>Ki;
		cout<<"Kd"<<endl;
		cin>>Kd;
	}

	//scelta frequenza campionamento
	t_c = 50;
	do
	{
		sbagliato_tc = false;
		cout<<"La frequenza di campionamento è: "<<t_c<<" ms"<<endl;
		cout<<"Si vuole modificare la frequenza?"<<endl;
		cout<<"1 --> Si"<<endl;
		cout<<"2 --> No"<<endl;
		cin>>flag_cambio_tc;
		if(flag_cambio_tc!=1 && flag_cambio_tc!=2)
		{
			sbagliato_tc = true;
			cout<<"Il valore inserito non è tra i valori permessi"<<endl;
		}
	}while(sbagliato_tc);

	//definizione file di output
	ofstream filetemperatura;
	filetemperatura.open("temperatura.txt");
	if(!filetemperatura)
	{
		cerr<<"Errore nell'apertura del file temperatura.txt"<<endl;
		return -1;
	}
	ofstream filetempo;
	filetempo.open("tempo.txt");
	if(!filetempo)
	{
		cerr<<"Errore nell'apertura del file tempo.txt"<<endl;
		return -1;
	}

	//Controlli

	//Controllo On/Off
	if(scelta_mod == 1)
	{
		cout<<"Inizio ciclo On/Off"<<endl;
		while(!_kbhit())
		{
			DAQmxReadAnalogScalarF64(hTaskHandleIn,10.0,&Vin,0);		//lettura Vin (V)
			t_misurata = conversione_tensione_temperatura(Vin*1000.0);	//conversione Vin (mV) in t_mis
			if(t_misurata >= 120)
			{
				cout<<"Blocco forzato del codice per raggiungimento della temperatura massima (120 gradi Celsius)"<<endl;
				DAQmxWriteAnalogScalarF64(hTaskHandleOut,0,10.0,0.0,NULL); 

				//chiusura di tutti i task
				DAQmxStopTask(hTaskHandleIn);
				DAQmxClearTask(hTaskHandleIn);
				DAQmxStopTask(hTaskHandleOut);
				DAQmxClearTask(hTaskHandleOut);

				Sleep(3000);
				return 0;	//blocca il ciclo while
			}

			t=t+(t_c/1000);	//vogliamo t_c in secondi per aggiornare t

			//salvataggio dei valori nei file
			filetemperatura<<t_misurata<<endl;
			filetempo<<t<<endl;

			//stampa valori per controllo da console
			cout<<"Tempo: "<<t<<"\tTemperatura: "<<t_misurata<<endl;
			//controllo
			if(t_setpoint>t_misurata)
			{
				cout<<"Forno acceso"<<endl;
				DAQmxWriteAnalogScalarF64(hTaskHandleOut,0,10.0,Vout_onoff,NULL);
			}
			else
			{
				cout<<"Forno spento"<<endl;
				DAQmxWriteAnalogScalarF64(hTaskHandleOut,0,10.0,0,NULL);
			}

			Sleep(t_c);
		}
		filetemperatura.close();
		filetempo.close();
	}
	else if(scelta_mod == 2)
	{
		cout<<"Inizio ciclo PID"<<endl;
		while(!_kbhit())
		{
			DAQmxReadAnalogScalarF64(hTaskHandleIn,10.0,&Vin,0);	//lettura Vin (V)
			t_misurata = conversione_tensione_temperatura(Vin*1000.0);	//conversione Vin (mV) in t_mis
			if(t_misurata >= 120)
			{
				cout<<"Blocco forzato del codice per raggiungimento della temperatura massima (120 gradi Celsius)"<<endl;
				DAQmxWriteAnalogScalarF64(hTaskHandleOut,0,10.0,0.0,NULL); 

				//chiusura di tutti i task
				DAQmxStopTask(hTaskHandleIn);
				DAQmxClearTask(hTaskHandleIn);
				DAQmxStopTask(hTaskHandleOut);
				DAQmxClearTask(hTaskHandleOut);

				Sleep(3000);
				return 0;	//blocca il ciclo while
			}

			t=t+(t_c/1000);	//vogliamo t_c in secondi per aggiornare t

			//salvataggio dei valori nei file
			filetemperatura<<t_misurata<<endl;
			filetempo<<t<<endl;

			//stampa valori per controllo da console
			cout<<"Tempo: "<<t<<"\tTemperatura: "<<t_misurata<<endl;
			
			//controllo
			err_new = t_setpoint-t_misurata;
			
			//calcolo componente proporzionale
			Vp = Kp*err_new;

			//calcolo componente integrale
			sum = sum + (((err_new+err_old)/2)*(t_c/1000));
			Vi = Ki*sum;

			//calcolo componente differenziale
			Vd = Kd*((err_new-err_old)/(t_c/1000));

			err_old = err_new;
			Vout_pid = Vp+Vi+Vd;

			if(Vout_pid>10.0)
			{
				Vout_pid = 10.0;
			}
			else if(Vout_pid<0.0)
			{
				Vout_pid=0.0;
			}
			DAQmxWriteAnalogScalarF64(hTaskHandleOut,0,10.0,Vout_pid,NULL);

			Sleep(t_c);
		}
		filetemperatura.close();
		filetempo.close();
	}
	DAQmxWriteAnalogScalarF64(hTaskHandleOut,0,10.0,0.0,NULL); //stampa 0 nel file

	//chiusura di tutti i task
	DAQmxStopTask(hTaskHandleIn);
	DAQmxClearTask(hTaskHandleIn);
	DAQmxStopTask(hTaskHandleOut);
	DAQmxClearTask(hTaskHandleOut);
}
