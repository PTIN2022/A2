#!/usr/bin/python3
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id='servidores', clean_session=False)

def on_publish(client,userdata,result):
	print("Datos publicados \n")

def on_connect(client, userdata, flags, rc):
	client.subscribe(topic='servidores', qos=2)


client.on_publish = on_publish
client.on_connect = on_connect

client.connect("test.mosquitto.org", 1883, 60)

client.loop_start();               
 
payload = input('>')
while(payload != 'exit'): 
   client.publish("servidores",payload,2)
   payload = "ping"
      
client.disconnect()
	
	
