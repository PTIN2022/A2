#!/usr/bin/python3
import sys
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	client.subscribe(topic='servidores', qos=2)

# La respuesta al mensaje PUBLISH
def on_message(client, userdata, msg):
	print('###############################')
	print('topic: %s' % msg.topic + '\npayload: %s' % msg.payload + '\nQoS: %d' % msg.qos)

def main():
	client = mqtt.Client(client_id='servidores', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("test.mosquitto.org", 1883, 60)

# Llamada que bloquea los procesos de trafico de red y maneja reconnexiones
	client.loop_forever() 

if __name__ == '__main__':
	main()

sys.exit(0)
