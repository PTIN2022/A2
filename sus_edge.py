import sys
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print("Conectado "+client._client_id.decode("utf-8"))
	
	client.subscribe(topic='edge', qos=2)

# La respuesta al mensaje PUBLISH
def on_message(client, userdata, msg):

	print('###############################')
#print("Topic: "+msg.topic+" Payload: "+str(msg.payload)+" QoS: "+msg.qos)
	print('topic: %s' % msg.topic + '\npayload: %s' % msg.payload + '\nQoS: %d' % msg.qos)


def main():
	client = mqtt.Client(client_id='iot', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 1883, 60)

# Llamada que bloquea los procesos de trafico de red y maneja reconnexiones
	client.loop_forever() 

if __name__ == '__main__':
	main()

sys.exit(0)
