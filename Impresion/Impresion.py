import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates 
import xlrd
import numpy
from datetime import datetime


folder = input(  'Introdizca el path a la carpeta del archivo ')
file = input(  'Introdizca el nombre del archivo ')
path = folder+'/'+file
#print(path)
book = xlrd.open_workbook(path)
n = book.nsheets
sheet = book.sheet_by_index(0)
rows = sheet.nrows
columns = sheet.ncols
sensores = []
for i in range(columns):
	sensores.append([])
sensor_label = []
sensor_label_prom = []
dates = []

def Read_Data():												
	for j in range(columns):										#Se busca recorrer las columnas por coordenada j
		for i in range(rows):										#Se busca recorrer las filas por coordenada i
			if i != 0:										#Se omite la primera fila de documento debido a que se conoce el estándar del documento
				if j == 0:									#Se identifica la columna que contiene los datos de fecha
					cell_date = sheet.cell(i,j)						#Se obtiene el dato tipo str que se contiene en la celda con coordenadas (i,j)
					objDate = datetime.strptime(cell_date.value, "%Y-%m-%d %H:%M:%S")	#Se convierte a tipo datetime year-month-day hour:min:second
					dates.append(objDate)							#Se agrega el dato a la lista de fechas
				else:										#Se actúa en caso de que el dato no sea fecha
					cell_sensor = sheet.cell(i,j)						#Se obtiene el dato tipo int que se contiene en la celda con coordenadas (i,j)
					sensores[j-1].append(int(cell_sensor.value))				#Se agrega el dato a la lista [j-1] en el conjunto de listas de sensor  
	return 0
def Calc_Print():
	promedio = []												#Se declara una lista de valores promedio
	dates_val = matplotlib.dates.date2num(dates)								#Se convierte el dato tipo datetime a número interpretable por matplotlib
	fig, ax = plt.subplots()										#Se define una figura nueva
	for i in range(columns-1):										#Se utiliza el número de columnas con el fin de conocer la cantidad de datos
		promedio.append(np.mean(sensores[i]))								#Se agrega el valor del promedio de los datos del sensor i a la lista de promedios
		sensor_label.append('sensor'+str(i+1))								#Se agrega el valor de la etiqueta del sensor a la lista de sensores
		sensor_label_prom.append('sensor'+str(i+1)+'='+str(round(promedio[i],2))) 			#Se añade el valor del promedio del conjunto a la etiqueta con 2 decimales
		ax.plot_date(dates_val, sensores[i],linestyle='solid',label=sensor_label[i])			#Se realiza un plot con x=fechas,y=valor del sensor, etiqueta sensor
	
	ax.grid()	
	ax.legend()
	fig, ax = plt.subplots()
	ax.bar(sensor_label_prom, promedio,label='Promedio de Humedad',edgecolor='black',fill=1,color='red')
	ax.set_yscale('log')
	ax.set_ylim(min(promedio)-(min(promedio)*0.2), max(promedio)+(max(promedio)*0.2))

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

