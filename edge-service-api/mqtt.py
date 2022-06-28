
import os
import json
import paho.mqtt.publish as publish

from utils.db import db
from models.model import Estacion, Cargador, Vehiculo
from datetime import datetime, timedelta


EDGE_BROKER = os.getenv('MQTT_BROKER_URL', 'craaxkvm.epsevg.upc.es')
EDGE_PORT = int(os.getenv('MQTT_BROKER_PORT', 23702))

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
        
def process_Marca_Libre(idEstacion,idPuntoCarga,kwh,matricula):
	print("---------------------------------")
    print("Tratando Marca libre")
    i = Estacion.query.filter(Estacion.nombre_est == idEstacion).one_or_none()
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
	


def process_battery(bateria, id_matricula):
    print("---------------------------------")
    print("Tratando bateria vehículo")
    m = Vehiculo.query.filter(Vehiculo.matricula == id_matricula).one_or_none()
    if m:
        m.procentaje_bat = bateria
        db.session.commit()
        print(m.procentaje_bat)
        # TODO: subir al cloud
    else:
        print("Vehículo no encontrado")


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
    	# Expected: {"idPuntoCarga": 2, "matricula":"34543FGC"}
    	if "idPuntoCarga" in payload and "kwh" in payload and "matricula" in payload:
    		process_marca_libre(payload["idPuntoCarga"],payload["kwh"],payload["matricula"])
    	
    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")
