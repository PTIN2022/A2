import json

from utils.db import db
from datetime import datetime
from models.model import Reserva, Cliente, Vehiculo, ClienteSchema, Ticket, Mensaje, Consumo, Estacion, Cargador

AVERIAS = {
    0: "ok",
    1: "enchufe",
    2: "voltaje",
    3: "pantalla",
    4: "circuito interno"
}


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
        print("Cliente modificado")


def process_add_client_event(data):
    c = Cliente(data['nombre'], data['apellido'], data['email'], data['dni'], data['foto'], data['telefono'], data['username'], data['password'], data['saldo'])
    db.session.add(c)
    db.session.commit()
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
        print("Reserva eliminada")


def process_add_ticket_event(payload):
    s = Ticket(payload["fecha"], payload["asunto"], payload["mensaje"], payload["estado"], payload["id_cliente"])
    db.session.add(s)
    db.session.commit()
    print("Ticket creado")


def process_responder_ticket_event(payload):
    s = Mensaje(payload["contenido"], payload["date"], payload["id_usuari"], payload["id_ticket"])
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


def process_new_batt(payload):
    i = Vehiculo.query.filter(Vehiculo.matricula == payload["matricula"]).one_or_none()
    if i:
        i.procentaje_bat = payload['procentaje_bat']
        print("New Batt % updated")


def process_remove_vehiculo(payload):
    i = Vehiculo.query.filter(Vehiculo.matricula == payload["matricula"]).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        print("Remove vehiculo OK")


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


def process_punto_carga_estado(payload):
    c = Cargador.query.filter(Cargador.id_cargador == payload["cargador_id"]).one_or_none()
    if c:
        if not c.estado:
            c.estado = "ocupado"
        else:
            c.estado = "libre"

    e = Estacion.query.filter(Estacion.id_estacion == c.estacion_id ).one_or_none()
    total_ocupados = 0
    for cargador in e.cargadores:
        if cargador.estado:
            total_ocupados += 1

    e.ocupation_actual = total_ocupados
    db.session.commit()
    print("Cargador actualizado, Ocupacion actualizada")


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

    elif topic == "gesys/cloud/reservas/remove":
        if "id_reserva" in payload:
            process_remove_reserva(payload)

    elif topic == "gesys/cloud/soporte/add":
        needed_keys = ['id_ticket', 'mensaje', 'estado', 'asunto', 'fecha', 'id_cliente']
        if all(key in payload for key in needed_keys):
            process_add_ticket_event(payload)
        else:
            print("TICKET no tiene los expected keys")

    elif topic == "gesys/cloud/soporte/response":
        needed_keys = ['id_usuari', 'contenido', 'id_mensaje', 'date', 'id_ticket']
        if all(key in payload for key in needed_keys):
            process_responder_ticket_event(payload)
        else:
            print("MSG ticket no tiene los expected keys")

    elif topic == "gesys/cloud/soporte/remove":
        if "ticket_id" in payload:
            process_remove_ticket(payload)
        else:
            print("ticket remove no tiene los expected keys")

    elif topic == "gesys/cloud/soporte/message/remove":
        if "msg_id" in payload:
            process_remove_ticket_msg(payload)
        else:
            print("message remove no tiene los expected keys")

    elif topic == "gesys/cloud/clientes/vehiculo/edit":
        if "matricula" in payload and "procentaje_bat" in payload:
            process_new_batt(payload)
        else:
            print("vehiculo edit no tiene los expected keys")

    elif topic == "gesys/cloud/clientes/vehiculo/remove":
        if "matricula" in payload:
            process_remove_vehiculo(payload)
        else:
            print("vehiculo remove no tiene los expected keys")

    elif topic == "gesys/cloud/puntoCarga/averia":
        # Expected: {"idPuntoCarga": 2, "averia": 0}
        if "idPuntoCarga" in payload and "averia" in payload:
            process_averias(payload["idPuntoCarga"], payload["averia"])
        else:
            print("averia no tiene los expected keys")

    elif topic == "gesys/cloud/puntoCarga/consumo":
        # Expected: {"idPuntoCarga": 2, "kwh": 432, "matricula":"34543FGC"}
        if "idPuntoCarga" in payload and "kwh" in payload and "matricula" in payload:
            process_carga_final(payload["idPuntoCarga"], payload["kwh"], payload["matricula"])
        else:
            print("consumo no tiene los expected keys")

    elif topic == "gesys/cloud/puntoCarga/estado":
        if "ocupado" in payload and "cargador_id" in payload:
            process_punto_carga_estado(payload)
        else:
            print("vehiculo remove no tiene los expected keys")
    else:
        print("Mensaje recibido, pero nunca fue tratado...")

    print("=================================")
