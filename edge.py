import sys
import paho.mqtt.client as mqtt
import time

# callback después de establecer connexión
def on_connect(client, userdata, flags, rc):
	print('(%s)' % client._client_id.decode("utf-8"), 'connected to broker')
	client.subscribe(topic='IoT', qos=2)

# callback del mensaje recibido
def on_message(client, userdata, message):
	print('------------------------------')
	print('Data received!')
	print('topic: %s' % message.topic)
	print('payload: %s' % message.payload.decode("utf-8"))
	print('qos: %d' % message.qos)
	print('------------------------------')
	# guardamos mensje que pasaremos al cloud
	global mensaje
	mensaje = message.payload.decode("utf-8")

	
# callback después de publicar
def on_publish(client,userdata,result):
    print("Data published!")
    pass 

def main():
    # creamos subscriptor
    client = mqtt.Client(client_id='Edge', clean_session=False)
    
    # definimos funciones a realizar despues de establecer connexión y recepción de mensajes
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    
    # subscriptor de IoT
    client.connect(host='localhost', port=1883)
    client.loop_start()
    time.sleep(5)
    
    # publisher de cloud
    client.connect(host="broker-cn.emqx.io", port=1883)
    client.loop_start()
    client.publish('Edge',mensaje,2)
    time.sleep(5)

if __name__ == '__main__':
	main()

sys.exit(0)
