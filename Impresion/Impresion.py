import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates 
import xlrd
import numpy
from datetime import datetime


book = xlrd.open_workbook('HumidityReport2023-02-03.xls')
n = book.nsheets
print ('El num de hojas es' , n )
sheet = book.sheet_by_index(0)
rows = sheet.nrows
print ('El num de filas es' , rows )
dias = []
sensor1 = []
dates = []

def Rows_Print():
	for i in range(rows):
		if i != 0:
			cell_date = sheet.cell(i,0)
			cell_sensor1 = sheet.cell(i,1)
			objDate = datetime.strptime(cell_date.value, "%Y-%m-%d %H:%M:%S")
			print(type(cell_sensor1.value))
			dates.append(objDate)
			sensor1.append(int(cell_sensor1.value))
			
			#print(objDate)
	return 0

A = Rows_Print()
dates = matplotlib.dates.date2num(dates)
fig, ax = plt.subplots()
ax.plot_date(dates, sensor1)

ax.grid()




plt.show()
##Requesitos de formato en archivo de datos
##Cambiar formato de xlsx a xls // Substituir puntos por comas 	




