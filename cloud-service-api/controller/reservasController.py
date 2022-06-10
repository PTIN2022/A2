from utils.db import db
from models.reserva import Reserva, ReservaSchema
from models.estacion import Estacion
from models.cargador import Cargador, CargadorSchema
from datetime import datetime
import random


def get_all_reservas():
    i = Reserva.query.all()
    return ReservaSchema(many=True).dump(i)


def get_reservas_id(id):
    i = Reserva.query.filter(Reserva.id_reserva == id).one_or_none()
    j=[]
    if i:
        j = Cargador.query.filter(Cargador.id_cargador==i.id_cargador).one_or_none()
    return ReservaSchema().dump(i), j.estacion_id


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
    j=[]
    if i:
        j = Cargador.query.filter(Cargador.id_cargador==i.id_cargador).one_or_none()
    return ReservaSchema().dump(i), j.estacion_id


def get_reservas_dni(dni):
    i = Reserva.query.filter(Reserva.id_cliente == dni)
    j=[]
    if i:
        j = Cargador.query.filter(Cargador.id_cargador==i.id_cargador).one_or_none()
    return ReservaSchema().dump(i), j.estacion_id


def post_reserva(id_estacion, matricula, fecha_inicio_str, fecha_final_str, DNI):
    i = Estacion.query.filter(Estacion.nombre_est == id_estacion).one_or_none()
    cargador_encontrado = False
    if i:
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
                    i = Reserva(fecha_inicio_str, fecha_final_str, cargador.id_cargador, matricula, DNI)
                    db.session.add(i)
                    db.session.commit()
                    cargador_encontrado = True
                    return i.id_reserva
    if not cargador_encontrado:
        return None


def remove_reserva(id):
    i = Reserva.query.filter(Reserva.id_reserva == id).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False
