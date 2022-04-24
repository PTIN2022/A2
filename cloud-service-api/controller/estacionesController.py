#from models.incidencia import Incidencia, incidencia_schema
from utils.db import db

estacion_list_general = [
  {
    "estacion": "VG1",
    "direccion": "Av.Victor Balaguer 2",
    "kwh_max": 720,
    "kwh_now": 75,
    "ocupation_max": 32,
    "ocupation_now": 20,
    "surface_in_meters": 130,
    "boss": "Alfredo Manresa"
  },
  {
    "estacion": "VG2",
    "direccion": "Calle de les Empúries 2",
    "kwh_max": 640,
    "kwh_now": 20,
    "ocupation_max": 32,
    "ocupation_now": 5,
    "surface_in_meters": 130,
    "boss": "Pere Roca"
  }
]

estacion_list_especificio = [
  {
  "estacionId": 3,
  "estacion": "VG3",
  "cordenadas": {
    "latitud": 41.224115,
    "longitud": 1.73061
  },
  "imagen": "http://?????????/estacion/VG3.png",
  "kwh_max": 20000,
  "ocupation_max": 8,
  "ocupation_now": 4,
  "list_plaza": [
    {
      "id": 1,
      "kwh_usage": 372,
      "battery_status": 372,
      "battery_max": 800,
      "cliente": "peroivi"
    },
    {
      "id": 7,
      "kwh_usage": 372,
      "battery_status": 372,
      "battery_max": 800,
      "cliente": "peroivi"
    },
    {
      "id": 3,
      "kwh_usage": 372,
      "battery_status": 372,
      "battery_max": 800,
      "cliente": "peroivi"
    },
    {
      "id": 6,
      "kwh_usage": 372,
      "battery_status": 372,
      "battery_max": 800,
      "cliente": "peroivi"
    }
  ]
  },
  {
  "estacionId": 4,
  "estacion": "VG4",
  "cordenadas": {
    "latitud": 41.224115,
    "longitud": 1.73061
  },
  "imagen": "http://?????????/estacion/VG3.png",
  "kwh_max": 20000,
  "ocupation_max": 8,
  "ocupation_now": 4,
  "list_plaza": [
    {
      "id": 3,
      "kwh_usage": 372,
      "battery_status": 372,
      "battery_max": 800,
      "cliente": "peroivi"
    },
    {
      "id": 5,
      "kwh_usage": 372,
      "battery_status": 372,
      "battery_max": 800,
      "cliente": "peroivi"
    },
    {
      "id": 7,
      "kwh_usage": 372,
      "battery_status": 372,
      "battery_max": 800,
      "cliente": "peroivi"
    },
    {
      "id": 8,
      "kwh_usage": 372,
      "battery_status": 372,
      "battery_max": 800,
      "cliente": "peroivi"
    }
  ]
  }
]

def get_all_estaciones():
    return estacion_list_general

def get_estacion_by_id(id):
    for estacion in estacion_list_especificio:
        if "estacionId" in estacion:
            if estacion["estacionId"] == int(id):
                # arreglar esto, devuelve solo una incidencia no todas las de esa estacion
                return estacion
    return None

def delete_plaza(id, id_plaza):
    for estacion in estacion_list_especificio:
       if "estacionId" in estacion:
            if estacion["estacionId"] == int(id):
                print(estacion["list_plaza"])
                for plaza in estacion["list_plaza"]:
                    if "id" in plaza:
                        if plaza["id"] == int(id_plaza):
                            estacion["list_plaza"].remove(plaza)
                            return True
    return False

