import json

from utils.db import db
from datetime import datetime
from models.model import Reserva, Cliente, Vehiculo, ClienteSchema


def process_remove_cliente(data):
    c = Cliente.query.filter(Cliente.id_cliente == data["dni"]).one_or_none()
    if c:
        db.session.delete(c)
        db.session.commit()
        print("Cliente eliminado correctamente")
    else:
        print("Cliente no se pudo eliminar")


def process_edit_client_event(data):
    c = Cliente.query.filter(Cliente.id_cliente == data["dni"]).one_or_none()
    if c:
        c.nombre = data["nombre"]
        c.apellido = data["apellido"]
        c.email = data["email"]
        c.foto = data["foto"]
        c.telefono = data["telefono"]
        c.username = data["username"]
        c.password = data["password"]
        c.saldo = data["saldo"]
        db.session.commit()


def process_add_client_event(data):
    c = Cliente(data['nombre'], data['apellido'], data['email'], data['dni'], data['foto'], data['telefono'], data['username'], data['password'], data['saldo'])
    db.session.add(c)
    db.session.commit()
    print(ClienteSchema().dump(c))
    print("Cliente registrado")


def process_reserva_event(data):
    ini = datetime.strptime(data["fecha_entrada"], '%Y-%m-%dT%H:%M:%S')
    fin = datetime.strptime(data["fecha_salida"], '%Y-%m-%dT%H:%M:%S')
    r = Reserva(ini, fin, data["procetnaje_carga"], data["precio_carga_completa"], data["precio_carga_actual"], data["estado"], data["tarifa"], data["asistida"], data["estado_pago"], data["id_cargador"], data["id_vehiculo"], data["id_cliente"])
    db.session.add(r)
    db.session.commit()
    print("Reserva registrada.")


def process_add_vehiculo_event(data):
    v = Vehiculo(data["matricula"], data["procentaje_bat"], data["modelo"])
    db.session.add(v)
    db.session.commit()

    print("Vehiculo añadido")
    c = Cliente.query.filter(Cliente.id_cliente == data["cliente"]).one_or_none()
    if c:
        c.vehiculos.append(v)

    print("Vehiculo assignado")


def process_remove_reserva(payload):
    i = Reserva.query.filter(Reserva.id_reserva == payload["id_reserva"]).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()


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

    elif topic == "gesys/cloud/clientes":
        needed_keys = ['saldo', 'nombre', 'type', 'dni', 'username', 'vehiculos', 'apellido', 'id_usuari', 'telefono', 'email', 'foto', 'password']
        if all(key in payload for key in needed_keys):
            process_add_client_event(payload)
        else:
            print(needed_keys)
            print(payload.keys())
            print("Cliente no tiene los expected keys")

    elif topic == "gesys/cloud/clientes":
        needed_keys = ['saldo', 'nombre', 'type', 'dni', 'username', 'vehiculos', 'apellido', 'id_usuari', 'telefono', 'email', 'foto', 'password']
        if all(key in payload for key in needed_keys):
            process_edit_client_event(payload)
        else:
            print(needed_keys)
            print(payload.keys())
            print("Cliente no tiene los expected keys")

    elif topic == "gesys/cloud/clientes/vehiculo":
        needed_keys = ['matricula', 'procentaje_bat', 'cliente', 'modelo']
        if all(key in payload for key in needed_keys):
            process_add_vehiculo_event(payload)
        else:
            print("Vehiculo no tiene los expected keys")

    elif topic == "gesys/cloud/clientes/remove":
        if "dni" in payload:
            process_remove_cliente(payload)
        else:
            print("Cliente remove no tiene los expected keys")

    elif topic == "gesys/cloud/clientes/edit":
        if "id_reserva" in payload:
            process_remove_reserva(payload)
    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")
