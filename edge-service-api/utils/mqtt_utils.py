import os
import json
import paho.mqtt.publish as publish


def send_to_cloud(topic, payload):
    if type(payload) == dict:
        payload = json.dumps(payload)

    publish.single(topic,
                   payload,
                   hostname=os.getenv('MQTT_LOCAL_CLOUD_URL', 'test.mosquitto.org'),
                   port=int(os.getenv('MQTT_LOCAL_CLOUD_PORT', 1883)),
                   qos=2)
