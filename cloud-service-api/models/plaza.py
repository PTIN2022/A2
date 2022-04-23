from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

class Plaza(db.Model):

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    kwh_usage = db.Column(db.Integer, nullable=False) 
    battery_status = db.Column(db.Integer, nullable=False)
    battery_max = db.Column(db.Integer, nullable=False)
    cliente = db.Column(db.String(30), nullable=False)
    estacion_id = db.Column(db.Integer, db.ForeignKey("estacion.id"), nullable=False)
   
    def __init__(self, kwh_usage, battery_status, battery_max, cliente, estacion_id):
        self.kwh_usage = kwh_usage
        self.battery_status = battery_status
        self.battery_max = battery_max
        self.cliente = cliente
        self.estacion_id = estacion_id
    
class PlazaSchema(SQLAlchemyAutoSchema):
    #estacion= fields.Nested(EstacionSchema)
    class Meta:
        model = Plaza
