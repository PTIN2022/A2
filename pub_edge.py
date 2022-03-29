import paho.mqtt.client as mqtt

client = mqtt.Client(client_id='edge', clean_session=False)

def on_publish(client,userdata,result):
	print("Datos publicados \n")

def on_connect(client, userdata, flags, rc):
	print("Conectado "+client._client_id.decode("utf-8"))
		
	client.subscribe(topic='edge', qos=2)
	
client.on_publish = on_publish
client.on_connect = on_connect


client.connect("localhost", 1883, 60)

client.loop_start();               
 
payload = input('')
while(payload != 'exit'): 

   client.publish("edge",payload,2)
   payload = input('')
      
client.disconnect()
	
	
