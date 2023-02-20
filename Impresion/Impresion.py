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
			dates.append(objDate)
			sensor1.append(cell_sensor1.value)
			
			#print(objDate)
	return 0


#def Lista_Dia():
#	for i in range(rows):
#		if i != 0:
#			cell = sheet.cell(i,0)
#			dias.append(cell.value)
#			#print (cell.value)
#	return 0
#def Lista_Sensor1():
#	for i in range(rows):
#		if i != 0:
#			cell = sheet.cell(i,1)
#			sensor1.append(cell.value)
#			print (cell.value)
#	return 0
#def gen_hist():
#	hist, bin_edges = numpy.histogram(sensor1, bins=10)
	
	

A = Rows_Print()
dates = matplotlib.dates.date2num(dates)
matplotlib.pyplot.plot_date(dates, sensor1)
#fig0 = plt.plot(dias, sensor1)


#fig1 = plt.hist(sensor1, bins=8)
plt.show()

		




