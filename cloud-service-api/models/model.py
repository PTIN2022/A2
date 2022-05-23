from utils.db import db
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Averia(db.Model):

    id_averia = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(300))

    id_trabajador = db.Column(db.Integer, db.ForeignKey(
        'trabajador.id_usuari'), nullable=True)
    name_estacion = db.Column(db.String(20), db.ForeignKey(
        'estacion.nombre_est'), nullable=False)

    def __init__(self, fecha, estado, descripcion, id_estacion, id_trabajador=None):
        self.fecha = fecha
        self.estado = estado
        self.descripcion = descripcion
        self.id_trabajador = id_trabajador
        self.name_estacion = id_estacion

class AveriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Averia

class Aviso(db.Model):
    id_aviso = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(20), nullable=False)
    texto = db.Column(db.String(300), nullable=False)
    hora = db.Column(db.DateTime, nullable=False)

    id_reserva = db.Column(db.Integer, db.ForeignKey("reserva.id_reserva"), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_usuari"), nullable=False)

    def __init__(self, tipo,texto, hora, id_reserva,id_cliente): #need
        self.tipo = tipo
        self.texto = texto
        self.hora = hora
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente


class AvisoSchema(SQLAlchemyAutoSchema):
    # estacion= fields.Nested(EstacionSchema)
    class Meta:
        model = Aviso


class Incidencia(db.Model):

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_estacion = db.Column(db.String(20), nullable=False)  # TODO: foreing key
    ###################################### CHANGE ME #############################################
    # estacion_id = db.Column(db.Integer, db.ForeignKey("estacion.id_estacion"), nullable=False)
    fecha_averia = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    descripcion = db.Column(db.String(200))

    def __init__(self, id_estacion, fecha, estado, descripcion):
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_averia = fecha
        self.id_estacion = id_estacion


class IncidenciaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incidencia

class Mensaje(db.Model):

	id_mensaje = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
	contenido = db.Column(db.String(300), nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	id_usuari = db.Column(db.Integer, db.ForeignKey('usuari_t.id_usuari'), nullable=False)

	id_ticket = db.Column(db.Integer, db.ForeignKey(
		'ticket.id_ticket'), nullable=False)

	def __init__(self, contenido,date, id_usuari, id_ticket):
		self.contenido = contenido
		self.date = date
		self.id_usuari = id_usuari
		self.id_ticket = id_ticket

class MensajeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mensaje


class Pago(db.Model):
    id_pago = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_reserva = db.Column('id_reserva', db.ForeignKey('reserva.id_reserva'), nullable=False)
    id_cliente = db.Column('id_cliente', db.ForeignKey('cliente.id_usuari'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint(id_reserva, id_cliente),
        {},
    )
    estado = db.Column(db.String(30), nullable=False)

    def __init__(self, id_reserva, id_cliente, estado):
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.estado = estado

class PagoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pago


class Reserva(db.Model):

    id_reserva = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    fecha_entrada = db.Column(db.DateTime, nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False)
    procetnaje_carga = db.Column(db.Integer, nullable=False)
    precio_carga_completa = db.Column(db.FLOAT, nullable=False)
    precio_carga_actual = db.Column(db.FLOAT, nullable=False)
    estado = db.Column(db.Boolean, nullable=True)
    tarifa = db.Column(db.FLOAT, nullable=False)
    asistida = db.Column(db.Boolean, nullable=True)
    estado_pago = db.Column(db.Boolean, nullable=True)

    id_cargador = db.Column(db.Integer, db.ForeignKey("cargador.id_cargador"), nullable=False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey(
        "vehiculo.matricula"), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_usuari"), nullable=False)

    avisos = db.relationship("Aviso",  backref="reserva")

    def __init__(self, fecha_entrada, fecha_salida, procetnaje_carga, precio_carga_completa, precio_carga_actual, estado, tarifa, asistida, estado_pago, id_cargador, id_vehiculo, id_cliente):
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.procetnaje_carga = procetnaje_carga
        self.precio_carga_completa = precio_carga_completa
        self.precio_carga_actual = precio_carga_actual
        self.estado = estado
        self.tarifa = tarifa
        self.asistida = asistida
        self.estado_pago = estado_pago
        self.id_cargador = id_cargador
        self.id_vehiculo = id_vehiculo
        self.id_cliente = id_cliente

class ReservaSchema(SQLAlchemyAutoSchema):
    # estacion= fields.Nested(EstacionSchema)
    class Meta:
        model = Reserva


class Sesiones(db.Model):
	codigo = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
	inicio_sesion = db.Column(db.DateTime, nullable=False)
	final_sesion = db.Column(db.DateTime, nullable=False)

	id_trabajador = db.Column('id_trabajador', db.ForeignKey(
            'trabajador.id_usuari'), nullable=False)

	def __init__(self, inicio_sesion, final_sesion,id_trabajador):
		self.inicio_sesion = inicio_sesion
		self.final_sesion = final_sesion
		self.id_trabajador = id_trabajador

class SesionesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Sesiones

class Ticket(db.Model):

	id_ticket = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
	fecha = db.Column(db.DateTime, nullable=False)
	asunto = db.Column(db.String(30), nullable=False)
	estado = db.Column(db.String(30), nullable=False)
	mensaje = db.Column(db.String(300), nullable=False)

	id_cliente = db.Column('id_cliente', db.ForeignKey('cliente.id_usuari'), nullable=False)
	mensajes = db.relationship("Mensaje",  backref="ticket")

	def __init__(self, fecha, asunto, mensaje,estado, id_cliente):
		self.fecha = fecha
		self.asunto = asunto
		self.mensaje = mensaje
		self.estado = estado
		self.id_cliente = id_cliente


class TicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket



class Usuari_t(db.Model):

    id_usuari = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    dni = db.Column(db.String(15), nullable=False, unique=True)
    foto = db.Column(db.String(15), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    type=db.Column(db.String(50))

    mensajes = db.relationship("Mensaje",  backref="usuari_t")

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': type
    }

    def __init__(self, nombre, apellido, email,dni, foto, telefono, username, password):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.dni = dni
        self.foto = foto
        self.telefono = telefono
        self.username = username
        self.password = password

class Usuari_tSchema(SQLAlchemyAutoSchema):
    # estacion= fields.Nested(EstacionSchema)
    class Meta:
        model = Usuari_t

class Trabajador(Usuari_t):

    id_trabajador = db.Column('id_usuari', db.ForeignKey('usuari_t.id_usuari'), nullable=False, primary_key=True)
    __table_args__ = (
        db.PrimaryKeyConstraint(id_trabajador),
        {},
    )
    cargo = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(30), nullable=False)
    ultimo_acceso = db.Column(db.DateTime, nullable=False)
    question = db.Column(db.String(300), nullable=False)

    averia = db.relationship("Averia",  backref="trabajador")
    sesion = db.relationship("Sesiones",  backref="trabajador")

    id_estacion = db.Column(db.Integer, db.ForeignKey(
        'estacion.id_estacion'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'trabajador',
    }

    def __init__(self, nombre, apellido, email,dni, foto, telefono, username, password, cargo, estado, ultimo_acceso, question, id_estacion):
        super(Trabajador, self).__init__(nombre, apellido, email,dni, foto, telefono, username,password)
        self.cargo = cargo
        self.estado = estado
        self.ultimo_acceso = ultimo_acceso
        self.question = question
        self.id_estacion = id_estacion


class TrabajadorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trabajador



vehiculo_cliente = db.Table("vehiculo-cliente", 
    db.Column('matricula', db.ForeignKey('vehiculo.matricula'), nullable=False, primary_key=True),
    db.Column('id_cliente', db.ForeignKey('cliente.id_usuari'), nullable=False, primary_key=True)
)


class Vehiculo(db.Model):
    matricula = db.Column(db.String(25), nullable=False, primary_key=True)
    procentaje_bat = db.Column(db.Integer, nullable=False)

    reservas = db.relationship("Reserva",  backref="vehiculo")


    modelos = db.Column(db.String(100), db.ForeignKey("modelo.modelo"), nullable=False)

    def __init__(self, matricula, procentaje_bat,modelos):
        self.matricula = matricula
        self.procentaje_bat = procentaje_bat
        self.modelos = modelos

class VehiculoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vehiculo

class Cliente(Usuari_t):
    id_cliente = db.Column('id_usuari', db.ForeignKey('usuari_t.id_usuari'), nullable=False, primary_key=True)
    __table_args__ = (
        db.PrimaryKeyConstraint(id_cliente),
        {},
    )

    avisos = db.relationship("Aviso",  backref="cliente")
    reservas = db.relationship("Reserva",  backref="cliente")
    ticket = db.relationship("Ticket",  backref="cliente")

    vehiculos = db.relationship('Vehiculo', secondary=vehiculo_cliente, lazy='subquery', backref=db.backref('Cliente', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }

    def __init__(self, nombre, apellido, email,dni, foto, telefono, username, password):
        super(Cliente, self).__init__(nombre, apellido, email,dni, foto, telefono, username,password)

class ClienteSchema(SQLAlchemyAutoSchema):
    vehiculos = Nested(VehiculoSchema, many=True)
    class Meta:
        model = Cliente

class Modelo(db.Model):

	modelo = db.Column(db.String(100), nullable=False, primary_key=True)
	marca = db.Column(db.String(30), nullable=False)
	
	# potencia_carga --> si es true = Carga Rapida, False = Normal
	potencia_carga = db.Column(db.Boolean, nullable=True)
	capacidad = db.Column(db.FLOAT, nullable=False)

	vehiculo = db.relationship("Vehiculo",  backref="modelo")

	def __init__(self, modelo,marca, potencia_carga, capacidad):
		self.modelo = modelo
		self.marca = marca
		self.potencia_carga = potencia_carga
		self.capacidad = capacidad


class ModeloSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Modelo




class Horas(db.Model):
    id = db.Column(db.DateTime, nullable=False, primary_key=True)

    def __init__(self, date):  #,id_cargador
        self.id = date

class HorasSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Horas

class Cargador(db.Model):

    id_cargador = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(30), nullable=False)
    posicion = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)

    estacion_id = db.Column(db.Integer, db.ForeignKey("estacion.id_estacion"), nullable=False)
    reservas = db.relationship("Reserva",  backref="Cargador")

    def __init__(self, estado, posicion, tipo, estacion_id):
        self.estado = estado
        self.posicion = posicion
        self.tipo = tipo
        self.estacion_id = estacion_id


class CargadorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cargador

class Consumo(db.Model):
    id_cargador = db.Column(db.ForeignKey('cargador.id_cargador'), nullable=False, primary_key=True)
    id_horas = db.Column(db.ForeignKey('horas.id'), nullable=False, primary_key=True)
    potencia_consumida = db.Column(db.Integer, nullable=False)
    potencia_maxima = db.Column(db.Integer, nullable=False)

    def __init__(self, id_cargador, id_horas, potencia_consumida, potencia_maxima):
        self.id_cargador = id_cargador
        self.id_horas = id_horas
        self.potencia_consumida = potencia_consumida
        self.potencia_maxima = potencia_maxima

class ConsumoSchema(SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Consumo

promocion_estacion = db.Table('promocion-stacion',
    db.Column('id_estacion', db.ForeignKey('estacion.id_estacion'), nullable=False),
    db.Column('id_promo', db.ForeignKey('promociones.id_promo'), nullable=False)
)


class Estacion(db.Model):
    id_estacion = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    nombre_est = db.Column(db.String(20), nullable=False, unique = True) #unico
    latitud = db.Column(db.Integer, nullable=False)
    longitud = db.Column(db.Integer, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(300), nullable=False)
    potencia_contratada = db.Column(db.Integer, nullable=False)
    zona = db.Column(db.String(300), nullable=False)
    ocupation_actual = db.Column(db.Integer, nullable=False)
    potencia_usada = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)

    cargadores = db.relationship("Cargador",  backref="estacion")
    trabajadores = db.relationship("Trabajador",  backref="estacion")
    averia = db.relationship("Averia",  backref="estacion")

    #encargado = db.Column('id_trabajador', db.ForeignKey('trabajador.id_usuari'), nullable=True)

    def __init__(self, nombre_est, latitud, longitud, capacidad, direccion, potencia_contratada, zona, ocupation_actual, potencia_usada, telefono, ciudad, pais):  # encargado
        self.nombre_est = nombre_est
        self.latitud = latitud
        self.longitud = longitud
        self.capacidad = capacidad
        self.direccion = direccion
        self.potencia_contratada = potencia_contratada
        self.zona = zona
        self.ocupation_actual = ocupation_actual
        self.potencia_usada = potencia_usada
        self.telefono = telefono
        self.ciudad = ciudad
        self.pais = pais
        #self.encargado = encargado

class EstacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Estacion


class Promociones(db.Model):
    id_promo = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    descuento = db.Column(db.Integer, nullable=False)
    cantidad_usados = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)
    estaciones = db.relationship("Estacion", secondary=promocion_estacion, lazy='subquery', backref=db.backref('promociones', lazy=True))

    def __init__(self, descuento, cantidad_usados, fecha_inicio, fecha_fin, estado, descripcion):
        self.descuento = descuento
        self.cantidad_usados = cantidad_usados
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.descripcion = descripcion

class PromocionesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Promociones
