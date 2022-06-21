from utils.db import db
from models.model import Reserva, ReservaSchema, Estacion, Cliente, Vehiculo
from datetime import datetime
import random


def get_all_reservas():
    i = Reserva.query.all()
    return ReservaSchema(many=True).dump(i)


def get_reservas_id(id):
    i = Reserva.query.filter(Reserva.id_reserva == id).one_or_none()
    return ReservaSchema().dump(i)


def get_reservas_estacion(id_estacion):
    i = Estacion.query.filter(Estacion.nombre_est == id_estacion).one_or_none()
    reservas_desde_ahora = []
    if i:
        ahora = datetime.today()
        for cargador in i.cargadores:
            for reserva in cargador.reservas:
                if reserva.fecha_salida > ahora:
                    reservas_desde_ahora.append(ReservaSchema().dump(reserva))

    return reservas_desde_ahora


def get_reservas_matricula(matricula):
    i = Reserva.query.filter(Reserva.id_vehiculo == matricula)
    return ReservaSchema(many=True).dump(i)


def get_reservas_dni(dni):
    cl = Cliente.query.filter(Cliente.dni == dni).one_or_none()
    res = ReservaSchema(many=True).dump(cl.reservas)
    return res


def post_reserva(id_estacion, matricula, tarifa, asistida, porcentaje_carga, precio_carga_completa, precio_carga_actual, estado_pago, fecha_inicio_str, fecha_final_str, DNI):
    i = Estacion.query.filter(Estacion.nombre_est == id_estacion).one_or_none()
    cargador_encontrado = False
    cl = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    vh = Vehiculo.query.filter(Vehiculo.matricula == matricula).one_or_none()
    if not cl:
        return {"error": "cliente no existe"}

    if not vh:
        return {"error": "vehiculo no existe"}

    if i:
        if i.estado == "Inactiva":
            return {"error": "Station not available, may damaged."}
        random.shuffle(i.cargadores)  # Se hace un shuffle para que no siempre se use el mismo cargador para evitar el desgaste del mismo
        for cargador in i.cargadores:
            if not cargador_encontrado:
                cargador_ocupado = False
                for reserva in cargador.reservas:
                    if not cargador_ocupado:
                        reserva = ReservaSchema().dump(reserva)
                        reserva_inicio_data = datetime.strptime(reserva["fecha_entrada"], '%Y-%m-%dT%H:%M:%S')
                        reserva_final_data = datetime.strptime(reserva["fecha_salida"], '%Y-%m-%dT%H:%M:%S')

                        if reserva_inicio_data <= fecha_inicio_str < reserva_final_data or reserva_inicio_data < fecha_final_str <= reserva_final_data:
                            cargador_ocupado = True
                        if fecha_inicio_str <= reserva_inicio_data < fecha_final_str or fecha_inicio_str < reserva_final_data <= fecha_final_str:
                            cargador_ocupado = True

                if not cargador_ocupado:
                    i = Reserva(
                        fecha_inicio_str, fecha_final_str, porcentaje_carga, precio_carga_completa, precio_carga_actual,
                        True, float(tarifa), asistida, estado_pago, cargador.id_cargador, matricula, cl.id_usuari
                    )
                    db.session.add(i)
                    db.session.commit()
                    cargador_encontrado = True
                    return i.id_reserva

    if not cargador_encontrado:
        return {"error": "no hay cargador libre en este horario"}


def remove_reserva(id):
    i = Reserva.query.filter(Reserva.id_reserva == id).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False
