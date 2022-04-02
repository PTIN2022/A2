import sys
import paho.mqtt.client as mqtt

# callback después de establecer connexión
def on_connect(client, userdata, flags, rc):
	print('(%s)' % client._client_id.decode("utf-8"), 'connected to broker')
	client.subscribe(topic='IoT/electrolinera/#', qos=2)

# callback del mensaje recibido
def on_message(client, userdata, message):
	print('------------------------------')
	print('Data received!')
	print('topic: %s' % message.topic)
	print('payload: %s' % message.payload.decode("utf-8"))
	print('qos: %d' % message.qos)
	print('------------------------------')

def main():
    # creamos suscriptor
    client = mqtt.Client(client_id='Cloud', clean_session=False)
    
    # definimos funciones a realizar despues de establecer connexión y recepción de mensajes
    client.on_connect = on_connect
    client.on_message = on_message
    
    # establecemos connexión
    client.connect(host="mqtt.fluux.io", port=1883)
    client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)
