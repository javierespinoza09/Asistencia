import numpy as np
import matplotlib.pyplot as plt
import xlrd

book = xlrd.open_workbook('Prueba.xls')
n = book.nsheets
print ('El num de hojas es' , n )
sheet = book.sheet_by_index(0)
rows = sheet.nrows
print ('El num de filas es' , rows )
dias = []
sensor1 = []

def Lista_Dia():
	for i in range(rows):
		if i != 0:
			cell = sheet.cell(i,0)
			dias.append(cell.value)
			#print (cell.value)
	return 0
def Lista_Sensor1():
	for i in range(rows):
		if i != 0:
			cell = sheet.cell(i,1)
			sensor1.append(cell.value)
			print (cell.value)
	return 0
A = Lista_Dia()
A = Lista_Sensor1()

plt.plot(dias, sensor1) 
plt.show()

		




