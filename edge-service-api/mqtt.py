import json
from utils.db import db
import paho.mqtt.publish as publish
from models.model import Estacion, Reserva, ReservaSchema
from datetime import datetime, timedelta


EDGE_BROKER = "test.mosquitto.org"
EDGE_PORT = 1883
QOS = 2


def process_camera_event(matricula, id_estacio):
    print("---------------------------------")
    print("Tratando proceso de camara")
    i = Estacion.query.filter(Estacion.nombre_est == id_estacio).one_or_none()
    if i:
        ahora = datetime.today()
        for cargador in i.cargadores:
            for reserva in cargador.reservas:
                if reserva.id_vehiculo == matricula:
                    if (reserva.fecha_entrada - timedelta(minutes=5)) < ahora < reserva.fecha_salida:
                        print("Hay una reserva valida, abriendo barrera...")
                        publish.single("gesys/estaciones/{}/camara".format(id_estacio),
                                       payload="1", qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)
                        return
    else:
        print("Estacion no encontrada...")

    print("Reserva no encontrada mandando no abrir barrera...") # TODO: useless?
    publish.single("gesys/estaciones/{}/camara".format(id_estacio),
                   payload="0", qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)


def deniseMethod(id_punto_carga, averia):
    pass


def process_msg(topic, raw_payload):
    print("=================================")
    print("TOPIC: {}".format(topic))
    print("PAYLOAD: {}".format(raw_payload))

    payload = None
    try:
        payload = json.loads(raw_payload)
    except json.decoder.JSONDecodeError:
        print("#MQTT EXCEPTION PAYLOAD IS NOT A JSON")
        return

    if topic == "gesys/edge/camara":
        # Expected: {"matricula": "34543FGC", "id_estacio": "VG1"}
        if "matricula" in payload and "id_estacio" in payload:
            process_camera_event(payload["matricula"], payload["id_estacio"])

    elif topic == "gesys/edge/puntoCarga/averia":
        # Expected: {"idPuntoCarga": 2, "averia": 0}
        if "idPuntoCarga" in payload and "averia" in payload:
            deniseMethod(payload["idPuntoCarga"], payload["averia"])
    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")