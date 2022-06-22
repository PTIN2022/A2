import os
import json
import paho.mqtt.publish as publish

from utils.db import db
from models.model import Estacion, Cargador, Vehiculo, Consumo
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


def process_battery(bateria, id_matricula):
    print("---------------------------------")
    print("Tratando bateria vehículo")
    m = Vehiculo.query.filter(Vehiculo.matricula == id_matricula).one_or_none()
    if m:
        for reserva in m.reservas:
            if reserva.id_vehiculo == id_matricula: 
            
                print("Porcentaje bateria ")
                m.procentaje_bat = bateria
                publish.single("gesys/edge/vehiculo/{matricula}".format(id_matricula),
                                       payload=m.procentaje_bat, qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)
                print("Porcentaje bateria: "+m.procentaje_bat)
                return
                # db.session.commit()
            
                # TODO: subir al cloud
    else:
        print("Vehículo no encontrado")
        

def process_carga_final(id_carga, consum, id_matricula):
    print("---------------------------------")
    print("Tratando consumo final del vehículo")
    c = Consumo.query.filter(Consumo.id_cargador == id_carga).one_or_none()
    v = Vehiculo.query.filter(Vehiculo.matricula == id_matricula).one_or_none()
    if c and v:
        c.potencia_consumida = consum
        db.session.commit()
        print(c.potencia_consumida)
        # TODO: subir al cloud
    else:
        print("Cargador no encontrado")
        
        
def process_punto_carga(id_carga, id_matricula):
    print("---------------------------------")
    print("Comprobando que el vehículo está en el cargador adecuado")
    c = Cargador.query.filter(Cargador.id_cargador == id_carga).one_or_none()
    v = Vehiculo.query.filter(Vehiculo.matricula == id_matricula).one_or_none()
    # Tenemos el vehículo con la matrícula 
    # Si existe ese vehículo por cada reserva que tiene el vehículo comprobamos
    # Si la reserva de ese vehículo está en el cargador que le toca:
    if v and c:
        for reserva in v.reservas:
            if reserva.id_cargador ==  id_carga:
            
                c.estado = "ocupado"
    
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
        # Expected: {"idPuntoCarga": 2, "kwh": 432,"matricula":"34543FGC"}
        if "idPuntoCarga" in payload and "consum" in payload and "matricula" in payload:
            process_carga_final(payload["idPuntoCarga"], payload["consum"], payload["matricula"])
            
    elif topic == "gesys/edge/puntoCarga/vehiculo":
        # Expected: {"idPuntoCarga": 2, "matricula":"34543FGC"}
        if "idPuntoCarga" in payload and "matricula" in payload:
            process_punto_carga(payload["idPuntoCarga"], payload["matricula"])
            
    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")
