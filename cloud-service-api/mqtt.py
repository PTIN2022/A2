import json

from utils.db import db
from datetime import datetime
from models.model import Reserva


def process_reserva_event(data):
    ini = datetime.strptime(data["fecha_entrada"], '%Y-%m-%dT%H:%M:%S')
    fin = datetime.strptime(data["fecha_salida"], '%Y-%m-%dT%H:%M:%S')
    r = Reserva(ini, fin, data["procetnaje_carga"], data["precio_carga_completa"], data["precio_carga_actual"], data["estado"], data["tarifa"], data["asistida"], data["estado_pago"], data["id_cargador"], data["id_vehiculo"], data["id_cliente"])
    db.session.add(r)
    db.session.commit()
    print("Reserva registrada.")


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

    if topic == "gesys/cloud/reservas":
        needed_keys = ["fecha_entrada", "id_cargador", "procetnaje_carga",
                       "precio_carga_completa", "estado","precio_carga_actual",
                       "id_cliente","id_reserva","asistida","fecha_salida",
                       "id_vehiculo","tarifa","estado_pago"]
        if all(key in payload for key in needed_keys):
            process_reserva_event(payload)
        else:
            print("Reserva no tiene los expected keys")

    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")
