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
  "fecha_averia": "2022-04-18",
  "id": 1,
  "id_estacion": "VG1"
}, {
  "descripcion": "El cargador de la planta 2 m plaza 1 no funciona",
  "estado": False,
  "fecha_averia": "2022-04-18",
  "id": 2,
  "id_estacion": "VG1"
}, {
  "descripcion": "El cargador de la planta 2 m plaza 1 no funciona",
  "estado": False,
  "fecha_averia": "2022-04-18",
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

    in_data["fecha_averia"] = "kjasdn"

    response = client.post("/incidencias", data=json.dumps(in_data), headers=headers)
    assert response.status_code == 400
    assert response.json == { "error": "Malformed request syntax."}

def test_get_incidencia_by_name(client):
    response = client.get("/incidencias/byname/VG1")
    assert response.status_code == 200
    assert response.json == out_data
    response = client.get("/incidencias/byname/MEH")
    assert response.status_code == 404
    assert response.json == { "error": "Incidencia not found."}

def test_get_incidencias_by_id(client):
    response = client.get("/incidencias/1")
    assert response.status_code == 200
    assert response.json == out_data[0]
    response = client.get("/incidencias/666")
    assert response.status_code == 404
    assert response.json == { "error": "Incidencia not found."}

def test_remove_incidencia(client):
    response = client.delete("/incidencias/666")
    assert response.status_code == 404
    assert response.json == { "error": "Incidencia not found." }

    response = client.delete("/incidencias/3")
    assert response.status_code == 200
    assert response.json == { "msg": "Data deleted correctly."}

    out_data.pop(2)

def test_modify_incidencia(client):
    response = client.put("/incidencias/666", data=json.dumps({"estado": "false"}), headers=headers)
    assert response.status_code == 404
    assert response.json == { "error": "Incidencia not found." }
    
    response = client.put("/incidencias/2", data=json.dumps({"estado": "true"}), headers=headers)
    assert response.status_code == 200
    out_data[1]["estado"] = True
    assert response.json == out_data[1]

    response = client.get("/incidencias/2")
    assert response.status_code == 200
    assert response.json == out_data[1]

    response = client.put("/incidencias/2", data=json.dumps({"fecha_averia": "2312344234"}), headers=headers)
    assert response.status_code == 400
    assert response.json == {"error": "Malformed request syntax."}

    response = client.put("/incidencias/2", data=json.dumps({"descripcion": "no va bien", "estacion": "VG2222", "fecha_averia":"20/07/2020"}), headers=headers)
    assert response.status_code == 200
    out_data[1]["descripcion"] = "no va bien"
    out_data[1]["id_estacion"] = "VG1"
    out_data[1]["fecha_averia"] = "2020-07-20"
    assert response.json == out_data[1]
