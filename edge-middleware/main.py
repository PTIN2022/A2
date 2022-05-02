#!/usr/bin/python
import json
import paho.mqtt.client as mqtt


client = mqtt.Client(client_id='edge1', clean_session=False)

def on_publish(client, userdata, result):
    print("Data published!")

# callback despues de establecer connexion
def on_connect(client, userdata, flags, rc):
    print('(%s)' % client._client_id.decode("utf-8"), 'connected to broker')
    client.subscribe("edge/1/#")
    client.subscribe("estacion/200/#")
        

# callback del mensaje recibido
def on_message(client, userdata, message):
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
                


def main():
    # creamos suscriptor

    # definimos funciones a realizar despues de establecer connexion y recepcion de mensajes
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    # establecemos connexion
    client.connect(host="test.mosquitto.org", port=1883) # BrokerCloud
    client.loop_forever()


if __name__ == '__main__':
    main()
