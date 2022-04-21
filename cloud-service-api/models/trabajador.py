from utils.db import db

class Trabajador(db.Model):

    DNI = db.Column(db.String(9), nullable=False, primary_key=True)
    name = db.Column(db.String(30), nullable=False) 
    lastname = db.Column(db.String(50), nullable=False)
    telf = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(320), nullable=False)
    rol = db.Column(db.String(20), nullable=False) #TODO: tabla errores foreign key
    last_access = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(300), nullable=False)

    def __init__(self, DNI, name, lastname, telf, email, rol, last_access, picture):
        self.DNI = DNI
        self.name = name
        self.lastname = lastname
        self.telf = telf
        self.email = email
        self.rol = rol
        self.last_access = last_access
        self.picture = picture

    def to_dict (self):
        return { "DNI": self.DNI, "name": self.name, "lastname": self.lastname, "telf": self.telf, "email": self.email, "rol": self.rol, "last_access": int(self.last_access), "picture": self.picture} 

