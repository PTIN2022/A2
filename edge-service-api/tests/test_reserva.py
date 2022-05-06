

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}
in_data1 = {
  "estacion": "VG3",
  "fecha_inicio": "18-04-2022 09:00",
  "fecha_final": "18-04-2022 17:00",
  "matricula": "LKE2378",
  "DNI": "1238712N"
}
in_data2 = {
  "estacion": "VG3",
  "fecha_inicio": "18-04-2022 09:00",
  "fecha_final": "18-04-2022 17:00",
  "matricula": "LKE2378",
  "DNI": "1238712N"
}
in_data3 = {
  "estacion": "VG3",
  "fecha_inicio": "18-04-2022 10:00",
  "fecha_final": "18-04-2022 11:00",
  "matricula": "LKE2378",
  "DNI": "1238712N"
}
in_data4 = {
  "estacion": "VG3",
  "fecha_inicio": "18-04-2022 08:00",
  "fecha_final": "18-04-2022 18:00",
  "matricula": "LKE2378",
  "DNI": "1238712N"
}
def test_post_incidencia(client):

    response = client.post("/reservas", data=json.dumps(in_data1), headers=headers)
    assert response.status_code == 200
    assert response.json != "{}"
    response = client.post("/reservas", data=json.dumps(in_data2), headers=headers)
    assert response.status_code == 200
    assert response.json != "{}"
    response = client.post("/reservas", data=json.dumps(in_data3), headers=headers)
    assert response.status_code == 200
    assert response.json == "{}"
    response = client.post("/reservas", data=json.dumps(in_data4), headers=headers)
    assert response.status_code == 200
    assert response.json == "{}"