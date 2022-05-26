import sqlalchemy
from models.model import EstacionSchema, Estacion, Horas, HorasSchema, Consumo, ConsumoSchema
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_all_estadisticas():
    est = Estacion.query.all()
    if est:
        estacion_total = {}
        estacion_total["estaciones"] = []
        results = Horas.query.order_by(sqlalchemy.desc(Horas.id)).all()
        data_inicio = HorasSchema().dump(results[-1])
        data_final = HorasSchema().dump(results[0])
        print(data_inicio)
        print(data_final)
        date_inicio_aux = datetime.strptime(data_inicio["id"], '%Y-%m-%dT%H:%M:%S').date()
        date_final_aux = datetime.strptime(data_final["id"], '%Y-%m-%dT%H:%M:%S').date()
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
                            cons = Consumo.query.filter(Consumo.id_cargador == cargador.id_cargador, Consumo.id_horas == hora.id).one_or_none()
                            if cons:
                                cons_obj = ConsumoSchema().dump(cons)
                                potencia_ej = int(cons_obj["potencia_consumida"])
                                if potencia_max_cons < potencia_ej:
                                    potencia_max_cons = potencia_ej
                date_inicio_str = date_inicio_str + relativedelta(days=1)
                data_inicio = str(date_inicio_str)
                new_estacion_json["dias"].append({'dia': data_inicio, 'potencia_max_cons': potencia_max_cons})
            new_estacion_json["estacion"] = estacion_dict["nombre_est"]
            new_estacion_json["direccion"] = estacion_dict["direccion"]
            new_estacion_json["kwh_max"] = estacion_dict["kwh_max"]
            new_estacion_json["kwh_now"] = estacion_dict["kwh_now"]
            estacion_total["estaciones"].append(new_estacion_json)
        return estacion_total
    else:
        return {}


def get_estadisticas_by_estacion(id, data_inicio, data_final):
    e = Estacion.query.filter(Estacion.id_estacion == id).one_or_none()
    if e:
        estacion_dict = EstacionSchema().dump(e)
        new_estacion_json = {}
        new_estacion_json["dias"] = []
        data = {}
        potencia_max_cons = 0
        for cargador in e.cargadores:
            c_list = Consumo.query.filter(Consumo.id_cargador == cargador.id_cargador and Consumo.id_horas > date_inicio and Consumo.id_horas < data_final)
            for cons in c_list:
                print(c.id_horas)
                c = ConsumoSchema().dump(cons)
                

        new_estacion_json["estacion"] = estacion_dict["nombre_est"]
        new_estacion_json["direccion"] = estacion_dict["direccion"]
        new_estacion_json["kwh_max"] = estacion_dict["potencia_contratada"]
        new_estacion_json["kwh_now"] = estacion_dict["potencia_usada"]
        return new_estacion_json
    else:
        return None
