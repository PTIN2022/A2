#!/usr/bin/python
import json
import paho.mqtt.client as mqtt


edge = mqtt.Client(client_id='edge2', clean_session=False)
cloud = mqtt.Client(client_id='edge1', clean_session=False)

def on_publish(client, userdata, result):
    print("Data published!")

# callback despues de establecer connexion
def on_connect_edge(client, userdata, flags, rc):
    print('(%s)' % client._client_id.decode("utf-8"), 'connected to broker')
    client.subscribe("estacion/200/#") # Faltaria que sea dinamico ?
    client.subscribe("coche/#") # Faltaria que sea dinamico ?
        

# callback del mensaje recibido
def on_message_edge(client, userdata, message):
    print('------------------------------')
    print('Data received!')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload.decode("utf-8"))
    print('qos: %d' % message.qos)
    print('------------------------------')

    if message.topic == "estacion/200":
        msg = json.loads(message.payload.decode("utf-8"))
        if "type" in msg:
            if msg["type"] == "cargador":
                print("Save Data bbdd")
                client.publish("cloud/estacion/200", json.dumps(msg), 2)
    if message.topic == "coche":
        if msg["type"] == "coche":
            print("Save Data bbdd")
            #client.publish("cloud/estacion/200", json.dumps(msg), 2)

def on_message_cloud(client, userdata, message):
    print('------------------------------')
    print('Data received!')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload.decode("utf-8"))
    print('qos: %d' % message.qos)
    print('------------------------------')

def on_connect_cloud(client, userdata, flags, rc):
    print('(%s)' % client._client_id.decode("utf-8"), 'connected to broker')
    client.subscribe("edge/1/#") # Get variable entorno


def main():
    # creamos suscriptor

    # definimos funciones a realizar despues de establecer connexion y recepcion de mensajes
    edge.on_connect = on_connect_edge
    edge.on_publish = on_publish
    edge.on_message = on_message_edge

    cloud.on_connect = on_connect_cloud
    cloud.on_publish = on_publish
    cloud.on_message = on_message_cloud

    # establecemos connexion
    edge.connect(host="test.mosquitto.org", port=1883) # BrokerEDGE
    cloud.connect(host="test.mosquitto.org", port=1883) # BrokerEDGE
    edge.loop_start()
    cloud.loop_forever()


if __name__ == '__main__':
    main()
