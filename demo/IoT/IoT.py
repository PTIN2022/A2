import paho.mqtt.client as mqtt
import time

# creamos el publicador
client = mqtt.Client(client_id='127.0.0.1', clean_session=False)

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
host       = "0.0.0.0"
port       = 1883

# Establecemos conexión
client.connect(host,port)

# Ejecutamos en loop
client.loop_start();                   

# Definimos el el quality of service
QOS        = 2                  
topic = 'IoT/'

time.sleep(1)
while True:
	# input del dato
	topic_name = topic + input('Enter topic: ')
	payload = input('Enter test text: ')
	print(topic_name)
	# publicamos el dato
	client.publish(topic_name,payload,QOS)
	time.sleep(2)
        
client.disconnect()
