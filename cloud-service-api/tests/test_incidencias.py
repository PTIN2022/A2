import json
from utils.errors import malformed_error

in_data = {
  "estacion": "VG1",
  "direccion": "Av.Victor Balaguer 2",
  "fecha_averia": "18/04/2022",
  "descripcion": "El cargador de la planta 2 m plaza 1 no funciona"
}

out_data = [{
  "descripcion": "El cargador de la planta 2 m plaza 1 no funciona",
  "estado": False,
  "fecha": "2022-04-18",
  "id": 1,
  "id_estacion": "VG1"
}, {
  "descripcion": "El cargador de la planta 2 m plaza 1 no funciona",
  "estado": False,
  "fecha": "2022-04-18",
  "id": 2,
  "id_estacion": "VG1"
}, {
  "descripcion": "El cargador de la planta 2 m plaza 1 no funciona",
  "estado": False,
  "fecha": "2022-04-18",
  "id": 3,
  "id_estacion": "VG1"
}]

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def test_get_all_incidencias_empty(client):
    response = client.get("/incidencias")
    assert response.status_code == 200
    assert response.json == []


def test_post_incidencia(client):

    response = client.post("/incidencias", data=json.dumps({}), headers=headers)
    assert response.status_code == 400
    assert response.json == malformed_error()

    response = client.post("/incidencias", data=json.dumps(in_data), headers=headers)
    assert response.status_code == 200
    assert response.json == out_data[0]


def test_get_all_incidencias_one(client):
    response = client.get("/incidencias")
    assert response.status_code == 200
    assert response.json == [out_data[0]]


def test_post_2_incidencias(client):
    response = client.post("/incidencias", data=json.dumps(in_data), headers=headers)
    assert response.status_code == 200
    assert response.json == out_data[1]

    response = client.post("/incidencias", data=json.dumps(in_data), headers=headers)
    assert response.status_code == 200
    assert response.json == out_data[2]
