from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Trabajador(db.Model):
    dni = db.Column(db.String(9), nullable=False, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    telf = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(320), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    last_access = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.String(300), nullable=False)
    id_estacion = db.Column(db.String(20), db.ForeignKey("estacion.nombre_est"), nullable=False)

    def __init__(self, dni, name, lastname, telf, email, rol, password, last_access, picture, estacion):
        self.dni = dni
        self.name = name
        self.lastname = lastname
        self.telf = telf
        self.email = email
        self.rol = rol
        self.password = password
        self.last_access = last_access
        self.picture = picture
        self.id_estacion=estacion


class TrabajadorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trabajador
        include_fk = True
        exclude = ('password',)
