from models.cargador import CargadorSchema
from models.consumo import Consumo, ConsumoSchema
from models.estacion import Estacion, EstacionSchema
from models.horas import Horas, HorasSchema
from datetime import datetime
from utils.db import db
from dateutil.relativedelta import relativedelta
import sqlalchemy


def get_all_estadisticas():
    est = Estacion.query.all()
    if est:
        estacion_total = {}
        estacion_total["estaciones"] = []
        results = Horas.query.order_by(sqlalchemy.desc(Horas.dia)).all()
        data_inicio = HorasSchema().dump(results[-1])
        data_final = HorasSchema().dump(results[0])
        date_inicio_aux = datetime.strptime(data_inicio['dia'], '%Y-%m-%d').date()
        date_final_aux = datetime.strptime(data_final['dia'], '%Y-%m-%d').date()
        for i in est:
            estacion_dict = EstacionSchema().dump(i)
            new_estacion_json = {}
            new_estacion_json["dias"] = []
            date_inicio_str = date_inicio_aux
            date_final_str = date_final_aux
            while date_inicio_str <= date_final_str:
                potencia_max_cons = 0
                for cargador in i.cargadores:
                    for hora in cargador.horas:
                        if hora.dia == date_inicio_str:
                            cons = Consumo.query.filter(Consumo.id_cargador==cargador.id_cargador, Consumo.id_horas==hora.id).one_or_none()
                            if cons:
                                cons_obj = ConsumoSchema().dump(cons)
                                potencia_ej = int(cons_obj["potencia_consumida"])
                                if potencia_max_cons < potencia_ej:
                                    potencia_max_cons = potencia_ej
                date_inicio_str = date_inicio_str + relativedelta(days=1)
                data_inicio = str(date_inicio_str)
                new_estacion_json["dias"].append({ 'dia': data_inicio, 'potencia_max_cons': potencia_max_cons })
            new_estacion_json["estacion"] = estacion_dict["nombre_est"]
            new_estacion_json["direccion"] = estacion_dict["direccion"]
            new_estacion_json["kwh_max"] = estacion_dict["kwh_max"]
            new_estacion_json["kwh_now"] = estacion_dict["kwh_now"]
            estacion_total["estaciones"].append(new_estacion_json)
        return estacion_total
    else:
        return {}


def get_estadisticas_by_estacion(id, data_inicio, data_final):
    i = Estacion.query.filter(Estacion.id_estacion == id).one_or_none()
    if i:
        estacion_dict = EstacionSchema().dump(i)
        new_estacion_json = {}
        new_estacion_json["dias"] = []
        while data_inicio <= data_final:
            potencia_max_cons = 0
            for cargador in i.cargadores:
                for hora in cargador.horas:
                    if hora.dia == data_inicio:
                        cons = Consumo.query.filter(Consumo.id_cargador==cargador.id_cargador, Consumo.id_horas==hora.id).one_or_none()
                        if cons:
                            cons_obj = ConsumoSchema().dump(cons)
                            potencia_ej = int(cons_obj["potencia_consumida"])
                            if potencia_max_cons < potencia_ej:
                                potencia_max_cons = potencia_ej
            date_inicio_str=str(data_inicio)
            new_estacion_json["dias"].append({ 'dia': date_inicio_str, 'potencia_max_cons': potencia_max_cons })
            data_inicio = data_inicio + relativedelta(days=1)
        new_estacion_json["estacion"] = estacion_dict["nombre_est"]
        new_estacion_json["direccion"] = estacion_dict["direccion"]
        new_estacion_json["kwh_max"] = estacion_dict["kwh_max"]
        new_estacion_json["kwh_now"] = estacion_dict["kwh_now"]
        return new_estacion_json
    else:
        return None
