from sensores_funciones import *
import time
import board
import busio
import digitalio
from analogio import AnalogIn
import adafruit_rfm9x
import sys

#a = sensores_varios()
#b = sensor_velocidad()
#c = sensor_precipitacion()

#data= [a[0],a[1],a[2],b,c]
####################################################################################
# Declaración de pines
####################################################################################
# Declara el uso del LED built-in (integrado) en el Feather M0
# Pin #13
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
uart = busio.UART(board.TX, board.RX, baudrate=9600)
####################################################################################
# Funciones
####################################################################################
# Función para el LED indicador de estatus: recibe el pin, el delay entre parpadeos
# y las veces que parpadea.
def blink(led, delay, veces):
    for i in range(0, veces):
        led.value = True
        time.sleep(delay)
        led.value = False
        time.sleep(delay)

def datos_sensores_meteorologicos():
    a = sensores_varios()
    b = sensor_velocidad()
    c = sensor_precipitacion()
    data= [a[0],a[1],a[2],a[3],a[4],a[5],b,c]
    # Se forma el paquete a enviar. Se empaquetan los datos separados por un "/" para distinguirlos
    data = (
        'Temperatura:'+ "/"+ data[0]+ "/"+ 'Humedad:'+ "/"+ data[1]+ "/"+ 'Presion:'+ "/"+ data[2]+ "/"
        + 'Altitud:'+ "/"+ data[3]+ "/"+ 'Luz:'+ "/"+ data[4]+ "/"+ 'Direccion de viento:'+ "/"+ data[5]
        + "/"+ 'Velocidad de viento:'+ "/"+ data[6]+ "/"+ 'Direccion de viento:'+ "/"+ data[7]
    )
    return data


####################################################################################
# Configuración del módulo de radio built-in Feather M0 RFM95
####################################################################################

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip.
# set GPIO pins as necessary - this example is for Feather M0 RFM9x
# CircuitPython build:
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 20

# Enable CRC checking
rfm9x.enable_crc = True
# Reintentos de envío del paquete antes de reportar un fallo
rfm9x.ack_retries = 10
# Delay entre el envío de cada ACK
rfm9x.ack_delay = 0.2
# Tiempo de espera del ack cuando se envía un mensaje
rfm9x.ack_wait = 1
rfm9x.xmit_timeout = 0.2
# Dirección del nodo
# 1 byte (0 a 255)
# Cambiar según el número de nodo de la red
rfm9x.node = 56
# Dirección del Gateway o destino
# 1 byte (0 a 255)
rfm9x.destination = 50

####################################################################################
# Ciclo infinito
###################################################################################
def send_ack(destination):
    rfm9x.destination = destination
    rfm9x.send(b"ok")


def rec_ack():
    packet = rfm9x.receive(
        with_ack=False, with_header=True, timeout=10.0, keep_listening=True
    )
    if packet is not None:
        if packet[4:] == b"ok":
            return True
        else:
            return False
    else:
        return False


# Siempre espera paquetes y envía el dato cuando se lo pide el Gateway, a menos que lo manden a dormir!
while True:
    print("Esperando mensajes...")
    # Espera por un nuevo paquete: solo acepta si está dirigido a este Nodo
    packet = rfm9x.receive(
        with_ack=False, with_header=True, timeout=10.0, keep_listening=True
    )
    # Si no se recibe un paquete durante el Timeout, se retorna None.
    if packet is not None:
        x = [hex(x) for x in packet[0:4]]
        print("Hay un mensaje de parte de: {}".format(packet[1]))

        # Verifica si la dirección de destino (byte 1 del Header) del paquete recibido corresponde a este nodo
        if x[0] != hex(rfm9x.node):
            continue
        # Si la dirección corresponde, retorna el paquete y responde según la acción
        else:
            # Se ha recibido un paquete: debería ser la solicitud del Gateway de los datos de humedad
            # Intenta decodificar el paquete en "ascii", si ocurre un error retorna al while mediante el continue
            try:
                paquete = str(packet[4:], "ascii")
            except:
                continue
            print("Received (raw header):", x)
            # print("Received (raw payload): {0}".format(packet[4:]))
            print("Received (payload): {0}".format(paquete))
            print("RSSI: {0}".format(rfm9x.last_rssi))
            # Se recibe la solicitud explícita Data!{Gateway Address} de parte del Gateway
            if paquete == "Data!{0}".format(rfm9x.node):
                print("Solicitud de flujo de parte de: {}".format(x[1]))
                send_ack(int(packet[1]))
                # Colecta los datos de los sensores
                # Se indican los pines digitales de alimentación
                data = datos_sensores_meteorologicos()
                print("Datos a enviar: {}".format(data))
                # Se envía el paquete de datos (lectura de los 4 sensores) al Gateway
                rfm9x.send(bytes(data, "UTF-8"))
                ack = rec_ack()
                print("Acknowledge {}".format(ack))
                blink(led, 0.1, 1)
