import sys
import paho.mqtt.client as mqtt
import time


# callback después de establecer connexión
def on_connect_sub(client, userdata, flags, rc):
    print('(%s)' % client._client_id.decode("utf-8"), 'connected to broker')
    client.subscribe(topic='IoT/#', qos=2)


def on_connect_pub(client, userdata, flags, rc):
    print('(%s)' % client._client_id.decode("utf-8"), 'connected to broker')


# callback del mensaje recibido
def on_message(client, userdata, message):
    print('------------------------------')
    print('Data received!')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload.decode("utf-8"))
    print('qos: %d' % message.qos)
    print('------------------------------')
    # guardamos mensje que pasaremos al cloud

    client2 = mqtt.Client(client_id='Edge_pub', clean_session=False)

    client2.on_connect = on_connect_pub
    client2.on_publish = on_publish

    client2.connect(host="broker-cloud", port=1883)
    client2.loop_start()
    client2.publish(message.topic, message.payload.decode("utf-8"), 2)
    time.sleep(3)

    client2.disconnect()


# callback después de publicar
def on_publish(client, userdata, result):
    print("Data published!")
    pass


def main():
    # creamos subscriptor
    client = mqtt.Client(client_id='Edge_sub', clean_session=False)
    # definimos funciones a realizar despues de establecer connexión y recepción de mensajes
    client.on_connect = on_connect_sub
    client.on_message = on_message
    client.on_publish = on_publish

    # subscriptor de IoT
    client.connect(host='broker-edge', port=1883)

    # publisher de cloud
    client.loop_forever()


if __name__ == '__main__':
    main()

sys.exit(0)
