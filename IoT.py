import paho.mqtt.client as mqtt
import time

# creamos el publicador
client = mqtt.Client(client_id='IoT', clean_session=False)

# callback después de publicar
def on_publish(client,userdata,result):
    print("Data published!")
    pass 

# callback después de establecer connexión
def on_connect(client, userdata, flags, rc):
	print(client._client_id.decode("utf-8"), 'ready to send data')
            

client.on_publish = on_publish
client.on_connect = on_connect

# indicamos host donde correremos el subscriptor y el puerto de comunicación
host       = "localhost"
port       = 1883

# Establecemos conexión
client.connect(host,port)

# Ejecutamos en loop
client.loop_start();                   

# Definimos el filtro (topic) para indicar a donde mandanos los datos y el quality of service
topic_name = "IoT"
QOS        = 2                  

time.sleep(1)
# input del dato
payload = input('Enter test text: ') 
# publicamos el dato
client.publish(topic_name,payload,QOS)
time.sleep(2)
        
client.disconnect()
