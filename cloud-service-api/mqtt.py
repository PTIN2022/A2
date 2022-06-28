import os
import json
import paho.mqtt.publish as publish

from utils.db import db
from models.model import Estacion, Cargador, Vehiculo, Consumo
from datetime import datetime, timedelta


CLOUD_BROKER = os.getenv('MQTT_BROKER_URL', 'test.mosquitto.org')
CLOUD_PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))

QOS = 2

AVERIAS = {
    0: "ok",
    1: "enchufe",
    2: "voltaje",
    3: "pantalla",
    4: "circuito interno"
}


def process_estado(estado, cargador_id):
    print("---------------------------------")
    print("Tratando estado cargador")
    cargador = Cargador.query.filter(Cargador.id_cargador == cargador_id).one_or_none()
    if not cargador:
    	print("Cargador not found")
        return
    
    else
    	if estado == True:
    		cargador.estado = "ocupado"
    		print("Estado")
    		print("Cargador marcado como ocupado")
    	else
    		cargador.estado = "libre"
    		print("Estado")
    		print("Cargador marcado como libre")
    		
    	db.session.commit()
		print("---------------------------------")
		print(c.estado)

def process_averia(idPuntoCarga,averia):
	print("---------------------------------")
    print("Tratando averias")
    c = Cargador.query.filter(Cargador.id_cargador == idPuntoCarga).one_or_none()
    if c:
        c.estado = AVERIAS[averia]
        db.session.commit()
        print(c.estado)
    else:
        print("Cargador no encontrado")
		
def process_consumo(idPuntoCarga,consumo):
	print("---------------------------------")
    print("Tratando consumo cargador")
	c = Consumo.query.filter(Consumo.id_cargador == id_carga, Consumo.id_horas == date).one_or_none()
    if not c:
        e = Estacion.query.filter(Estacion.id_estacion == cargador.estacion_id).one_or_none()
        c = Consumo(id_carga, date, 0, e.potencia_contratada)
        db.session.add(c)
        print("Consumo no encontrado.... Creandolo...")
        db.session.commit()
        
    potencia_anterior = c.potencia_consumida
    c.potencia_consumida = c.potencia_consumida+consumo
    db.session.commit()
    print("Registrando consumo del cargador: {} -- Potencia consumida anterior: {} -- Potencia consumida={}".format(c.id_cargador, potencia_anterior, c.potencia_consumida))	




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

    if topic == "gesys/cloud/puntoCarga/estado":
        # Expected: {"ocupado": "True", "cargador_id": "2"}
        if "ocupado" in payload and "cargador_id" in payload:
            process_estado(payload["ocupado"], payload["cargador_id"])
	
	if topic == "gesys/cloud/puntoCarga/consumo":
		# Expected: {"idPuntoCarga": 2, "kwh": 432 }
		if "idPuntoCarga" in payload and "kwh" in payload:
            process_consumo(payload["idPuntoCarga"], payload["kwh"])
            
    if topic == "gesys/cloud/puntoCarga/averia":
    	# Expected: {"idPuntoCarga": 2, "averia": 0}
		if "idPuntoCarga" in payload and "averia" in payload:
            process_averia(payload["idPuntoCarga"], payload["averia"])
		
    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")
