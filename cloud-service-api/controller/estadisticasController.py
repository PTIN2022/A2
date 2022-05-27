import sqlalchemy
from models.model import EstacionSchema, Estacion, Horas, HorasSchema, Consumo, ConsumoSchema
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_all_estadisticas():
    est_cons_list = []
    est_list = Estacion.query.all()
    for e in est_list:
        estacion_dict = EstacionSchema().dump(e)
        new_estacion_json = {}
        new_estacion_json["dias"] = []
        data = {}
        potencia_max_cons = 0
        for cargador in e.cargadores:
            c_list = Consumo.query.filter(Consumo.id_cargador == cargador.id_cargador and Consumo.id_horas > date_inicio and Consumo.id_horas < data_final)
            for cons in c_list:
                
                print(ConsumoSchema().dump(cons))
                key = cons.id_horas.strftime("%Y-%m-%d")
                if key in data:
                    if cons.potencia_consumida > data[key]["potencia_max_cons"]:
                        data[key]["potencia_max_cons"] = cons.potencia_consumida
                        
                else:
                    data[key] = {}
                    data[key]["dia"] = key
                    data[key]["potencia_max_cons"] = cons.potencia_consumida

        new_estacion_json["dias"] = list(data.values())
        new_estacion_json["estacion"] = estacion_dict["nombre_est"]
        new_estacion_json["direccion"] = estacion_dict["direccion"]
        new_estacion_json["kwh_max"] = estacion_dict["potencia_contratada"]
        new_estacion_json["kwh_now"] = estacion_dict["potencia_usada"]
        est_cons_list.append(new_estacion_json)
   
    return est_cons_list 

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
                
                print(ConsumoSchema().dump(cons))
                key = cons.id_horas.strftime("%Y-%m-%d")
                if key in data:
                    if cons.potencia_consumida > data[key]["potencia_max_cons"]:
                        data[key]["potencia_max_cons"] = cons.potencia_consumida
                        
                else:
                    data[key] = {}
                    data[key]["dia"] = key
                    data[key]["potencia_max_cons"] = cons.potencia_consumida

        new_estacion_json["dias"] = list(data.values())
        new_estacion_json["estacion"] = estacion_dict["nombre_est"]
        new_estacion_json["direccion"] = estacion_dict["direccion"]
        new_estacion_json["kwh_max"] = estacion_dict["potencia_contratada"]
        new_estacion_json["kwh_now"] = estacion_dict["potencia_usada"]
        return new_estacion_json
    else:
        return None
