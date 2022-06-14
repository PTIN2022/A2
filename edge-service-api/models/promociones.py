from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Promocion(db.Model):
    id_promo = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    descuento = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)
<<<<<<< Updated upstream
    
=======

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    def __init__(self, descuento, fecha_inicio, fecha_fin, estado, descripcion):
        self.descuento = descuento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.descripcion = descripcion


class PromocionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Promocion
