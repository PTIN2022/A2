#!/usr/bin/python3

# Autor: Xavier Mazon Borras
# Data: 26/03/2022

#Librerias
#import sys
#from struct import *
from socket import *

print("Valor a enviar al servidor: "+str(1234567890))

# Configuramos conexion al servidor, la IP esta a modo de ejemplo en el puerto 10000
serverName = ('192.168.1.67', 10000)

# El cliente prepara la conexion con el servidor con
# AF_INET -> IPv4
# SOCK_DGRAM | SOXK_STREAM => modo UDP | modo TCP
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Le decimos donde hay que conectarse
clientSocket.connect(serverName)
# Enviamos datos al servidor, que en este caso es el protocolo UDP
clientSocket.sendto(str(1234567890).encode(), serverName)
# Cerramos la conexion
clientSocket.close()
