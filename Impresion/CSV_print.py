import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates 
import csv
import numpy
from datetime import datetime
filas = []
datos = []
dato = ""
print("Hola mundo")
with open("HumidityReport2023-02-03.csv") as file:
	csvreader = csv.reader(file)
	header = next(csvreader)
	print (header)
	y=0
	for row in csvreader:
    		filas.append(row)	
print(filas[0][0])			
				
