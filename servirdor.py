#!/usr/bin/python3

# Autor: Xavier Mazon Borras
# Data: 26/03/2022

#Librerias
#import sys
#from struct import *
from socket import *

# Creacion del socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Establecemos que cualquier IP externa permite que establezca al puerto 10000
# esto es solo una prueba pero se puede cambiar de puerto y de IP
serverSocket.bind(('0.0.0.0', 10000))
# El servidor estara a la espera que algun cliente mande un mensaje de un tamaño
# estandard, configurable de 512 bytes a mas o menos
connection = serverSocket.recv(512)
print("Valor revicbido: "+str(connection.decode()))
# Cerramos la conexion 
serverSocket.close()
