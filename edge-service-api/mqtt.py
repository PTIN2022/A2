import os
import json
import paho.mqtt.publish as publish

from utils.db import db
from utils.mqtt_utils import send_to_cloud
from models.model import Estacion, Cargador, Vehiculo, Consumo, Mensaje, Ticket, Reserva, Trabajador
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


def process_responder_ticket_event(payload):
    s = Mensaje(payload["contenido"], datetime.strptime(payload["date"], "%Y-%m-%dT%H:%M:%S"), payload["id_usuari"], payload["id_ticket"])
    db.session.add(s)
    db.session.commit()
    print("Mensaje creado")


def process_remove_ticket(payload):
    s = Ticket.query.filter(Ticket.id_ticket == payload["ticket_id"]).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        print("Ticket Eliminado")


def process_remove_ticket_msg(payload):
    s = Mensaje.query.filter(Mensaje.id_mensaje == payload["msg_id"]).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        print("Mensaje eliminado")


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

    print("Reserva no encontrada mandando no abrir barrera...")
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
                    payload = {"battery": reserva.procetnaje_carga}
                    publish.single("gesys/vehiculo/{}/cargaMaxima".format(id_matricula), payload=json.dumps(payload), qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)
                    print("Porcentaje bateria: {}={}%".format(m.matricula, m.procentaje_bat))

                    payload = {"battery": bateria}
                    publish.single("gesys/vehiculo/{}".format(id_matricula), payload=json.dumps(payload), qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)
                    db.session.commit()
                    return
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


def process_reserva_event(data):
    ini = datetime.strptime(data["fecha_entrada"], '%Y-%m-%dT%H:%M:%S')
    fin = datetime.strptime(data["fecha_salida"], '%Y-%m-%dT%H:%M:%S')
    r = Reserva(ini, fin, data["procetnaje_carga"], data["precio_carga_completa"], data["precio_carga_actual"], data["estado"], data["tarifa"], data["asistida"], data["estado_pago"], data["id_cargador"], data["id_vehiculo"], data["id_cliente"])
    db.session.add(r)
    db.session.commit()
    print("Reserva registrada.")
    
def process_reserva_edit_event(data):
    r = Reserva.query.filter(Reserva.id_reserva == data["id_reserva"]).one_or_none()
    if r:
        r.fecha_entrada = data["fecha_entrada"]
        r.id_cargador = data["id_cargador"]
        r.procetnaje_carga = data["procetnaje_carga"]
        r.precio_carga_completa = data["precio_carga_completa"]
        r.estado = data["estado"]
        r.precio_carga_actual = data["precio_carga_actual"]
        r.asistida = data["asistida"]
        r.fecha_salida = data["fecha_salida"]
        r.id_vehiculo = data["id_vehiculo"]
        r.tarifa = data["tarifa"]
        r.estado_pago = data["estado_pago"]
        db.session.commit()
        print("Reserva modificada")


def process_remove_reserva(payload):
    i = Reserva.query.filter(Reserva.id_reserva == payload["id_reserva"]).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        print("Reserva eliminada")


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
    for reserva in v.reservas:
        if (reserva.fecha_entrada - timedelta(minutes=5)) < ahora < reserva.fecha_salida:
            if reserva.id_cargador == id_carga:
                print("Cargador ocupado por el coche que tenia la reserva")
                cargador.estado = "ocupado"
                send_to_cloud("gesys/cloud/puntoCarga/estado", {"ocupado": "ocupado", "cargador_id": cargador.id_cargador})
            else:
                print("Cargador ocupado por un coche sin reserva, (GRUA?)")

            payload = {"idPuntoCarga": reserva.id_cargador, "cargaLimiteCoche": reserva.procetnaje_carga}
            publish.single("gesys/puntoCarga/{}".format(id_carga), payload=json.dumps(payload), qos=QOS, hostname=EDGE_BROKER, port=EDGE_PORT)
            return

    print("El cargador {}, no tiene ninguna reserva, pero el coche {} esta ocupando la plaza. Llamando a la grua...".format(id_carga, id_matricula))


def process_new_trabajador(payload):
    t = Trabajador(payload["nombre"], payload["apellido"], payload["email"], payload["dni"], payload["foto"], payload["telefono"], payload["username"], payload["password"],
                   payload["cargo"], payload["estado"], datetime.strptime(payload["ultimo_acceso"], "%Y-%m-%dT%H:%M:%S"), payload["question"], payload["id_estacion"])

    db.session.add(t)
    db.session.commit()
    print("Trabajador añadido")


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
            send_to_cloud("gesys/cloud/puntoCarga/averia", payload)

    elif topic == "gesys/edge/vehiculo":
        # Expected: {"battery": 0, "matricula":"34543FGC"}
        if "battery" in payload and "matricula" in payload:
            process_battery(payload["battery"], payload["matricula"])

    elif topic == "gesys/edge/puntoCarga/consumo":
        # Expected: {"idPuntoCarga": 2, "kwh": 432, "matricula":"34543FGC"}
        if "idPuntoCarga" in payload and "kwh" in payload and "matricula" in payload:
            process_carga_final(payload["idPuntoCarga"], payload["kwh"], payload["matricula"])
            send_to_cloud("gesys/cloud/puntoCarga/estado", {"ocupado": "libre", "cargador_id": payload["idPuntoCarga"]})
            send_to_cloud("gesys/cloud/puntoCarga/consumo", payload)

    elif topic == "gesys/edge/puntoCarga/vehiculo":
        # Expected: {"idPuntoCarga": 2, "matricula":"34543FGC"}
        if "idPuntoCarga" in payload and "matricula" in payload:
            process_punto_carga(payload["idPuntoCarga"], payload["matricula"])

    elif topic == "gesys/edge/soporte/response":
        needed_keys = ['id_usuari', 'contenido', 'id_mensaje', 'date', 'id_ticket']
        if all(key in payload for key in needed_keys):
            process_responder_ticket_event(payload)
        else:
            print("MSG ticket no tiene los expected keys")

    elif topic == "gesys/edge/soporte/remove":
        if "ticket_id" in payload:
            process_remove_ticket(payload)

    elif topic == "gesys/edge/soporte/message/remove":
        if "msg_id" in payload:
            process_remove_ticket_msg(payload)

    elif topic == "gesys/edge/reservas":
        needed_keys = ["fecha_entrada", "id_cargador", "procetnaje_carga",
                       "precio_carga_completa", "estado", "precio_carga_actual",
                       "id_cliente", "id_reserva", "asistida", "fecha_salida",
                       "id_vehiculo", "tarifa", "estado_pago"]
        if all(key in payload for key in needed_keys):
            process_reserva_event(payload)
        else:
            print("Reserva no tiene los expected keys")
    
    elif topic == "gesys/edge/reservas/edit":
        needed_keys = ["fecha_entrada", "id_cargador", "procetnaje_carga",
                       "precio_carga_completa", "estado", "precio_carga_actual",
                       "id_cliente", "id_reserva", "asistida", "fecha_salida",
                       "id_vehiculo", "tarifa", "estado_pago"]
        if all(key in payload for key in needed_keys):
            process_reserva_edit_event(payload)
        else:
            print("Reserva no tiene los expected keys")

    elif topic == "gesys/edge/reservas/remove":
        if "id_reserva" in payload:
            process_remove_reserva(payload)

    elif topic == "gesys/edge/trabajador":
        needed_keys = ['apellido', 'id_trabajador', 'id_usuari',
                       'foto', 'id_estacion', 'telefono', 'email',
                       'nombre', 'question', 'type', 'dni', 'ultimo_acceso',
                       'cargo', 'estado', 'username', 'password', "id_estacion"]
        if all(key in payload for key in needed_keys):
            process_new_trabajador(payload)
        else:
            print("Trabajador no tiene los expected keys")
    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")
