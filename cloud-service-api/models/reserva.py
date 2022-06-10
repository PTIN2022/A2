from utils.db import db
# from models.vehiculo import Vehiculo
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Reserva(db.Model):

    id_reserva = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    fecha_entrada = db.Column(db.DateTime, nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False)
    # tiempo_consumido = db.Column(db.DateTime, nullable=False)
    # tiempo_restante = db.Column(db.DateTime, nullable=False)
    # precio_carga_completa = db.Column(db.FLOAT, nullable=False)
    # precio_carga_actual = db.Column(db.FLOAT, nullable=False)
    # estado = db.Column(db.String(30), nullable=False)
    id_cargador = db.Column(db.Integer, db.ForeignKey("cargador.id_cargador"), nullable=False)
    # id_vehiculo = db.Column(db.String(7), db.ForeignKey("vehiculo.id_vehiculo"), nullable=False) TODO
    id_vehiculo = db.Column(db.String(20), nullable=False)
    # id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_usuari"), nullable=False)
    id_cliente = db.Column(db.String(20), nullable=False)  # TODO: foreingk key
    # avisos = db.relationship("Aviso",  backref="reserva")

    # def __init__(self, fecha_entrada, fecha_salida, tiempo_consumido, tiempo_restante, precio_carga_completa, precio_carga_actual, estado, id_cargador, id_vehiculo, id_cliente):
    def __init__(self, fecha_entrada, fecha_salida, id_cargador, id_vehiculo, id_cliente):
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        # self.tiempo_consumido = tiempo_consumido
        # self.tiempo_restante = tiempo_restante
        # self.precio_carga_completa = precio_carga_completa
        # self.precio_carga_actual = precio_carga_actual
        # self.estado = estado
        self.id_cargador = id_cargador
        self.id_vehiculo = id_vehiculo
        self.id_cliente = id_cliente


class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        include_fk = True
