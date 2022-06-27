import os
import json
import paho.mqtt.publish as publish

from utils.db import db
from models.model import Estacion, Cargador, Vehiculo, Consumo
from datetime import datetime, timedelta


EDGE_BROKER = os.getenv('MQTT_BROKER_URL', 'test.mosquitto.org')
EDGE_PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))

QOS = 2

AVERIAS = {
    0: "ok",
    1: "enchufe",
    2: "voltaje",
    3: "pantalla",
    4: "circuito interno"
}


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
                        print("SEND: ABRIR")
                        return
    else:
        print("Estacion no encontrada...")

    print("Reserva no encontrada mandando no abrir barrera...")  # TODO: useless?
    publish.single("gesys/estaciones/{}/camara".format(id_estacio),
                   payload="0", qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)
    print("SEND: CERRAR")


def process_averias(id_carga, num_averia):
    print("---------------------------------")
    print("Tratando averias")
    c = Cargador.query.filter(Cargador.id_cargador == id_carga).one_or_none()
    if c:
        c.estado = AVERIAS[num_averia]
        db.session.commit()
        print(c.estado)
        # TODO: subir al cloud

    else:
        print("Cargador no encontrado")


def process_battery(bateria, id_matricula):
    print("---------------------------------")
    print("Tratando bateria vehículo")
    m = Vehiculo.query.filter(Vehiculo.matricula == id_matricula).one_or_none()
    if m:
        ahora = datetime.today()
        for reserva in m.reservas:
            if reserva.id_vehiculo == id_matricula:
                if (reserva.fecha_entrada - timedelta(minutes=5)) < ahora < reserva.fecha_salida:
                    m.procentaje_bat = bateria
                    payload = {"battery": m.procentaje_bat}
                    publish.single("gesys/vehiculo/{}".format(id_matricula), payload=json.dumps(payload), qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)
                    print("Porcentaje bateria: {}={}%".format(m.matricula, m.procentaje_bat))
                    db.session.commit()
                    return
                    # TODO: subir al cloud
        print("Reserva para este vehiculo no encontrada")
    else:
        print("Vehículo no encontrado")


def process_carga_final(id_carga, kwh, id_matricula):
    print("---------------------------------")
    print("Tratando consumo final del vehículo")
    date = datetime.now().replace(microsecond=0, second=0, minute=0)
    cargador = Cargador.query.filter(Cargador.id_cargador == id_carga).one_or_none()
    if not cargador:
        print("Cargador not found")
        return

    v = Vehiculo.query.filter(Vehiculo.matricula == id_matricula).one_or_none()
    if not v:
        print("Vehiculo no encontrado")
        return

    c = Consumo.query.filter(Consumo.id_cargador == id_carga, Consumo.id_horas == date).one_or_none()
    if not c:
        e = Estacion.query.filter(Estacion.id_estacion == cargador.estacion_id).one_or_none()
        c = Consumo(id_carga, date, 0, e.potencia_contratada)
        db.session.add(c)
        print("Consumo no encontrado.... Creandolo...")
        db.session.commit()

    potencia_anterior = c.potencia_consumida
    c.potencia_consumida = c.potencia_consumida+kwh
    c.estado = "libre"
    db.session.commit()
    print("Registrando consumo del cargador: {} -- Potencia consumida anterior: {} -- Potencia consumida={}".format(c.id_cargador, potencia_anterior, c.potencia_consumida))
    # TODO: subir al cloud


def process_punto_carga(id_carga, id_matricula):
    print("---------------------------------")
    print("Comprobando que el vehículo está en el cargador adecuado")
    cargador = Cargador.query.filter(Cargador.id_cargador == id_carga).one_or_none()
    if not cargador:
        print("Cargador not found")
        return

    v = Vehiculo.query.filter(Vehiculo.matricula == id_matricula).one_or_none()
    if not v:
        print("Vehiculo no encontrado, en el cargador {}, llamando a la grua...".format(id_carga))
        return

    # Tenemos el vehículo con la matrícula
    ahora = datetime.today()
    for reserva in cargador.reservas:
        if reserva.id_vehiculo == id_matricula:
            if (reserva.fecha_entrada - timedelta(minutes=5)) < ahora < reserva.fecha_salida:
                cargador.estado = "ocupado"
                payload = {"idPuntoCarga": cargador.id_cargador, "cargaLimiteCoche": reserva.procetnaje_carga}
                publish.single("gesys/edge/puntoCarga/{}".format(id_carga), payload=payload, qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)

    print("El cargador {}, no tiene ninguna reserva, pero el coche {} esta ocupando la plaza. Llamando a la grua...".format(id_carga, id_matricula))


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
            process_averias(payload["idPuntoCarga"], payload["averia"])

    elif topic == "gesys/edge/vehiculo":
        # Expected: {"battery": 0, "matricula":"34543FGC"}
        if "battery" in payload and "matricula" in payload:
            process_battery(payload["battery"], payload["matricula"])

    elif topic == "gesys/edge/puntoCarga/consumo":
        # Expected: {"idPuntoCarga": 2, "kwh": 432,"matricula":"34543FGC"}
        if "idPuntoCarga" in payload and "kwh" in payload and "matricula" in payload:
            process_carga_final(payload["idPuntoCarga"], payload["kwh"], payload["matricula"])

    elif topic == "gesys/edge/puntoCarga/vehiculo":
        # Expected: {"idPuntoCarga": 2, "matricula":"34543FGC"}
        if "idPuntoCarga" in payload and "matricula" in payload:
            process_punto_carga(payload["idPuntoCarga"], payload["matricula"])

    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")
