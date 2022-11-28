import time
import board
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_bh1750
import busio
import digitalio
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull

#Sensor de direccion de viento, variables
analog_in = AnalogIn(board.A1)

#Sensor de lluvia variables
bucket_size = 0.28 #mm por tick
count_hora = 0     #Contador de ticks del sensor
count_dia = 0      #Contador de tickes por día
global lista_conteos
lista_conteos = []
global lista_conteos_dia
lista_conteos_dia = []
global lista_precipitacion_hora
lista_precipitacion_hora = []
global lista_precipitacion_dia
lista_precipitacion_dia = []

#Anemómetro variables
speed = 2.4    #Un tick por segundo equivale a 2.4km/h
count_wind_speed = 0  #Lleva el conteo de ticks de la velocidad del viento
wind_speed = 0        #Variable para determinar la velocidad del viento
ban=False             #Se establece una bandera para iniciar el conteo
tiempoInicio_viento = time.monotonic()  #Establece el tiempo de inicio del conteo

digital_in = DigitalInOut(board.D11)    #Lee el pin digital D11


#Funciones para conteo de ticks del sensor de lluvia
digital_in = DigitalInOut(board.D10)    #Lee el pin digital D10

def get_voltage_dig(pin):
    return (pin.value * 3.3)

def ticks(): #Va a depender los ticks de lluvia que caigan, es una interrupcion
  global a
  #comp = int(input("Ingrese el valor de a :"))
  a = get_voltage_dig(digital_in)
  return a

def bucket_tipped_hora():  #Contador de los ticks por segundo, puede dar el volumen de lluvia
  global count_hora
  count_hora = count_hora + 1
  print(count_hora)
  time.sleep(1)

def bucket_tipped_dia():  #Contador de los ticks por segundo, puede dar el volumen de lluvia
  global count_dia
  count_dia = count_dia + 1
  print(count_dia)
  time.sleep(1)

def sensores_varios():
    print("Temperatura: ", bme280.temperature)
    print("Humedad: ", bme280.relative_humidity)
    print("Presión: ", bme280.pressure)
    print("Altitud: ", bme280.altitude)
    print("Luminosidad: ", sensor.lux)
    print("\n")
    data_Temp = uart.write(bytes(f"Temperatura: {bme280.temperature} °C", "ascii"))
    data_Humed = uart.write(bytes(f"\nHumedad: {bme280.relative_humidity} %", "ascii"))
    data_Pres = uart.write(bytes(f"\nPresión: {bme280.pressure} hPa", "ascii"))
    data_Alti = uart.write(bytes(f"\nAltitud: {bme280.altitude} mts", "ascii"))
    data_Lum = uart.write(bytes(f"\nLuminosidad: {sensor.lux} lx", "ascii"))
    data_Space = uart.write(bytes(f"\n", "ascii"))

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# OR create sensor object, using the board's default SPI bus.
# spi = board.SPI()
# bme_cs = digitalio.DigitalInOut(board.D10)
# bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25
i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)

uart = busio.UART(board.TX, board.RX, baudrate=9600)

tiempoInicio = time.monotonic()
tiempoInicio_dia = time.monotonic()
tiempoInicio_Sensores = time.monotonic()
condicionSalida = time.monotonic()
condicionSalida_dia = time.monotonic()
i = 1  #Contador de horas, indica la cantidad de horas que ha pasado
k = 1  #Contador de días que han pasado, indica la cantidad de días transcurridos, así se sabe que día es
count_hora = 0
lista_conteos.append("Día %d" %k)

while True:
    sensores_varios()