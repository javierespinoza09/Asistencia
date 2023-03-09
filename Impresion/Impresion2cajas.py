import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates 
import xlrd
import numpy
from datetime import datetime


folder = input(  'Introdizca el path a la carpeta del archivo ')
fileA = input(  'Introdizca el nombre del archivo con BC ')
pathA = folder+'/'+fileA

fileB = input(  'Introdizca el nombre del archivo sin BC ')
pathB = folder+'/'+fileB

#A > CON BC
#B > SIN BC

#print(path)
bookA = xlrd.open_workbook(pathA)
bookB = xlrd.open_workbook(pathB)
#n = book.nsheets
sheetA = bookA.sheet_by_index(0)
sheetB = bookB.sheet_by_index(0)

rowsA = sheetA.nrows
rowsB = sheetB.nrows
nDates = min([rowsA,rowsB])


columns = sheetA.ncols
sensoresA = []
sensoresB = []
sensorA_label = []
sensorB_label = []
for i in range(columns):
	sensoresA.append([])
	sensoresB.append([])
	sensorA_label.append(sheetA.cell(0,i).value)
	sensorB_label.append(sheetB.cell(0,i).value)
sensorA_label_prom = []
sensorB_label_prom = []
datesA = []
datesB = []

def Read_Data():												
	for j in range(columns):										#Se busca recorrer las columnas por coordenada j
		for i in range(nDates):										#Se busca recorrer las filas por coordenada i
			if i != 0:										#Se omite la primera fila de documento debido a que se conoce el estándar del documento
				if j == 0:									#Se identifica la columna que contiene los datos de fecha
					cell_date = sheetA.cell(i,j)						#Se obtiene el dato tipo str que se contiene en la celda con coordenadas (i,j)
					objDate = datetime.strptime(cell_date.value, "%Y-%m-%d %H:%M:%S")	#Se convierte a tipo datetime year-month-day hour:min:second
					datesA.append(objDate)
					cell_date = sheetB.cell(i,j)						#Se obtiene el dato tipo str que se contiene en la celda con coordenadas (i,j)
					objDate = datetime.strptime(cell_date.value, "%Y-%m-%d %H:%M:%S")	#Se convierte a tipo datetime year-month-day hour:min:second
					datesB.append(objDate)							#Se agrega el dato a la lista de fechas
				else:										#Se actúa en caso de que el dato no sea fecha
														#Se obtiene el dato tipo int que se contiene en la celda con coordenadas (i,j)
					sensoresA[j-1].append(int(sheetA.cell(i,j).value))				#Se agrega el dato a la lista [j-1] en el conjunto de listas de sensor 
					sensoresB[j-1].append(int(sheetB.cell(i,j).value))				#Se agrega el dato a la lista [j-1] en el conjunto de listas de sensor 
	return 0
def Calc_Print():
	promedioA = []												#Se declara una lista de valores promedio
	promedioB = []
	dates_valA = matplotlib.dates.date2num(datesA)								#Se convierte el dato tipo datetime a número interpretable por matplotlib
	dates_valB = matplotlib.dates.date2num(datesB)
	fig, ax = plt.subplots()										#Se define una figura nueva
	for i in range(3):										#Se utiliza el número de columnas con el fin de conocer la cantidad de datos
		promedioA.append(np.mean(sensoresA[i+2]))
		promedioB.append(np.mean(sensoresB[i+2]))								#Se agrega el valor del promedio de los datos del sensor i a la lista de promedios								
		sensorA_label_prom.append(sensorA_label[i+3]+' BC '+str(round(promedioA[i],2))) 			#Se añade el valor del promedio del conjunto a la etiqueta con 2 decimales
		sensorB_label_prom.append(sensorB_label[i+3]+' - '+str(round(promedioB[i],2)))
		ax.plot_date(dates_valA, sensoresA[i+2],linestyle='solid',label=sensorA_label[i+3]+'BC')			#Se realiza un plot con x=fechas,y=valor del sensor, etiqueta sensor
		ax.plot_date(dates_valB, sensoresB[i+2],linestyle='solid',label=sensorB_label[i+3]+'-')
	ax.set_ylabel("% Humedad")
	ax.set_xlabel("Tiempo")
	ax.grid()	
	ax.legend()
	fig, ax = plt.subplots()
	ax.bar(sensorA_label_prom, promedioA,label='Promedio de Humedad',edgecolor='black',fill=1,color='red')
	#ax.set_yscale('log')
	ax.set_ylim(min(promedioA)-(min(promedioA)*0.2), max(promedioA)+(max(promedioA)*0.2))
	
	ax.grid()
	ax.legend()
	
	fig, ax = plt.subplots()
	ax.bar(sensorB_label_prom, promedioB,label='Promedio de Humedad',edgecolor='black',fill=1,color='green')
	#ax.set_yscale('log')
	ax.set_ylim(min(promedioB)-(min(promedioB)*0.2), max(promedioB)+(max(promedioB)*0.2))

	ax.grid()
	ax.legend()
	


A = Read_Data()
A = Calc_Print()


#promedios = [np.mean,,,,]


#fig, ax = plt.subplots()
#ax.hist(sensor1)
#ax.grid()

plt.show()
##Requesitos de formato en archivo de datos
##Cambiar formato de xlsx a xls // Substituir puntos por comas 	

