#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
import random
from faker import Faker
from utils.db import db
from models.model import Estacion, Cliente, Trabajador, Promociones, PromocionEstacion, \
    Cargador, Modelo, Consumo, Horas, Vehiculo, Reserva, Cupon, Transaccion, Historial
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.utils import encrypt_password
import requests
from random import choices
from random import randint


def fakedata():
    fake = Faker()

    # ### Estaciones

    e = Estacion(  # , t.id_trabajador
        'VG1',
        41.217606,
        1.727072,
        32,
        "Rambla de L'exposicio",
        230,
        'Zona industrial',
        1,
        150,
        '+34762487248',
        'Vilanova i la geltru',
        'Espa\xc3\xb1a',
        'Activa'
        )
    db.session.add(e)
    e2 = Estacion(  # , t.id_trabajador
        'VG2',
        41.221002,
        1.730369,
        32,
        'Rambla de A',
        220,
        'Zona mayonesa',
        15,
        110,
        '+34762854712',
        'Vilanova i la geltru',
        'Espa\xc3\xb1a',
        'Activa'
        )
    db.session.add(e2)
    e3 = Estacion(  # , t.id_trabajador
        'VG3',
        41.225431,
        1.737627,
        32,
        'A veces',
        120,
        'Zona M de motomami',
        8,
        70,
        '+34785123478',
        'Vilanova i la geltru',
        'Espa\xc3\xb1a',
        'Activa'
        )
    db.session.add(e3)
    e4 = Estacion(  # , t.id_trabajador
        'VG4',
        41.227420,
        1.728166,
        32,
        'Rambla de Shrek',
        300,
        'Zona memes de baki',
        1,
        20,
        '+34745821523',
        'Vilanova i la geltru',
        'Espa\xc3\xb1a',
        'Activa'
        )
    db.session.add(e4)
    e5 = Estacion(  # , t.id_trabajador
        'VG5',
        41.229674,
        1.721478,
        32,
        'Casoplon del coletas',
        30,
        'Zona SEAX',
        14,
        15,
        '+34797458744',
        'Vilanova i la geltru',
        'Espa\xc3\xb1a',
        'Activa'
        )
    db.session.add(e5)
    e6 = Estacion(  # , t.id_trabajador
        'VG6',
        41.222119,
        1.718915,
        32,
        'Casa de ibai',
        45,
        'Zona el bicho',
        20,
        32,
        '+34768220011',
        'Vilanova i la geltru',
        'Espa\xc3\xb1a',
        'Activa'
        )
    db.session.add(e6)
    e7 = Estacion(  # , t.id_trabajador
        'VG7',
        41.223434,
        1.710113,
        32,
        'Rambla de Redes Multimedia',
        278,
        'Zona XAMU',
        26,
        190,
        '+34798544552',
        'Vilanova i la geltru',
        'Espa\xc3\xb1a',
        'Dañada'
        )
    db.session.add(e7)
    e8 = Estacion(  # , t.id_trabajador
        'VG8',
        41.217122,
        1.709477,
        32,
        'Bar pepin',
        200,
        'Zona vip',
        32,
        130,
        '+34768855471',
        'Vilanova i la geltru',
        'Espa\xc3\xb1a',
        'Inactiva'
        )
    db.session.add(e8)
    db.session.commit()
    estacioness = [
        e,
        e2,
        e3,
        e4,
        e5,
        e6,
        e7,
        e8,
        ]
    clientes = []
    ce = Cliente(
        "mario",
        "hola",
        "prueba@gmail.com",
        "123319N",
        "url",
        189237389,
        "mariuski",
        encrypt_password("1"),
        )
    db.session.add(ce)
    clientes.append(ce)

    db.session.commit()
    # ### CLIENTE
    for i in range(100):
        letras = [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'J',
            'K',
            'L',
            'M',
            'N',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'V',
            'W',
            'X',
            'Y',
            'Z',
            ]
        num = '{:08}'.format(random.randrange(1, 10 ** 8))
        dni = num + random.choice(letras)

        nombre = fake.first_name()
        apellido = fake.last_name()
        email = fake.free_email()

        foto = requests.get("https://100k-faces.glitch.me/random-image%22").url
        telefono = '{:09}'.format(random.randrange(1, 10 ** 8))
        username = nombre + num
        password = apellido + num

        ce = Cliente(
            nombre,
            apellido,
            email,
            dni,
            foto,
            telefono,
            username,
            encrypt_password(password),
            )
        db.session.add(ce)
        clientes.append(ce)

        db.session.commit()

    clienteBueno = Cliente(
        "The Client",
        "meh",
        "meh@meh.com",
        "23432234F",
        "X",
        2343234,
        "cli",
        "pass",
        )
    db.session.add(clienteBueno)
    clientes.append(clienteBueno)

    db.session.commit()
    # ### TRABAJADOR
    # Creamos 3 tipos de trabajadores

    trabajadores = []
    estacion = random.choice(estacioness)
    ultimo_acceso = fake.date_time_between(start_date='-2y', end_date='now')
    telefono = '{:09}'.format(random.randrange(1, 10 ** 8))
    tr = Trabajador(
        'Alfredo',
        'Manresa',
        'tugmail@adas',
        'a111111111',
        'asda',
        telefono,
        'alfredo',
        encrypt_password('1'),
        'administrador',
        'Activo',
        ultimo_acceso,
        'Amigo de la infancia?',
        estacion.id_estacion,
    )
    db.session.add(tr)
    trabajadores.append(tr)
    db.session.commit()
    estacion = random.choice(estacioness)
    ultimo_acceso = fake.date_time_between(start_date='-2y', end_date='now')
    telefono = '{:09}'.format(random.randrange(1, 10 ** 8))
    tr = Trabajador(
        'Marc',
        'Capdevila',
        'tugmail2@adas',
        'b222222222',
        'asda',
        telefono,
        'marc',
        encrypt_password('1'),
        'encargado',
        'Activo',
        ultimo_acceso,
        'Amigo de la infancia?',
        estacion.id_estacion,
    )
    db.session.add(tr)
    trabajadores.append(tr)
    db.session.commit()
    estacion = random.choice(estacioness)
    ultimo_acceso = fake.date_time_between(start_date='-2y', end_date='now')
    telefono = '{:09}'.format(random.randrange(1, 10 ** 8))
    tr = Trabajador(
        'Cinta',
        'Gonzalez',
        'tugmail3@adas',
        'c333333333',
        'asda',
        telefono,
        'marc',
        encrypt_password('1'),
        'trabajador',
        'Activo',
        ultimo_acceso,
        'Amigo de la infancia?',
        estacion.id_estacion,
    )
    db.session.add(tr)
    trabajadores.append(tr)
    db.session.commit()
    for i in range(100):
        letras = [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'J',
            'K',
            'L',
            'M',
            'N',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'V',
            'W',
            'X',
            'Y',
            'Z',
            ]
        num = '{:08}'.format(random.randrange(1, 10 ** 8))
        dni = num + random.choice(letras)
        nombre = fake.first_name()
        apellido = fake.last_name()
        email = fake.free_email()
        foto = requests.get("https://100k-faces.glitch.me/random-image%22").url
        telefono = '{:09}'.format(random.randrange(1, 10 ** 8))
        username = nombre + num
        password = apellido + num
        cargos = ['administrador', 'encargado', 'trabajador']
        estados = ['Activo', 'Inactivo']
        estado = random.choice(estados)
        estacion = random.choice(estacioness)
        cargo = random.choice(cargos)
        if estado == 'Activo':
            for worker in trabajadores:
                if worker.cargo == 'administrador' and worker.id_estacion == estacion.id_estacion:
                    cargo = 'trabajador'
                elif worker.cargo == 'encargado' and worker.id_estacion == estacion.id_estacion:
                    cargo = 'trabajador'
        ultimo_acceso = fake.date_time_between(start_date='-2y', end_date='now')
        tr = Trabajador(
            nombre,
            apellido,
            email,
            dni,
            foto,
            telefono,
            username,
            encrypt_password(password),
            cargo,
            estado,
            ultimo_acceso,
            'Amigo de la infancia?',
            estacion.id_estacion,
            )
        db.session.add(tr)
        trabajadores.append(tr)

        db.session.commit()

    # ### PROMOCIONES

    promociones = []
    for i in range(10):
        descuento = random.randint(0, 100)
        fecha_inicio = fake.date_time_between(start_date='-2y', end_date='now')
        fecha_fin = fake.date_time_between(start_date='-2y', end_date='now')
        estado = 'inactiva'
        descripcion = str(''.join(random.choices(string.ascii_uppercase
                          + string.digits, k=250)))

        p = Promociones(descuento, 0, fecha_inicio, fecha_fin, descripcion)
        db.session.add(p)
        promociones.append(p)
    db.session.commit()

    # ### PromocionEstacion
    for i in range(15):
        estacion = random.choice(estacioness)
        promo = random.choice(promociones)
        relation = PromocionEstacion(estacion.id_estacion, promo.id_promo, 'inactiva')
        db.session.add(relation)
        db.session.commit()

    # ### cupones:
    for c in clientes:
        estado = choices(['Usado', 'No usado'], [0.8, 0.2])
        letras = [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'J',
            'K',
            'L',
            'M',
            'N',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'V',
            'W',
            'X',
            'Y',
            'Z',
        ]
        num = '{:05}'.format(random.randrange(1, 10 ** 8))
        cupon = random.choice(letras) + num + random.choice(letras) + random.choice(letras)
        valor = random.randint(15, 30)
        cup = Cupon(valor, cupon, c.id_cliente, estado[0])
        db.session.add(cup)
    db.session.commit()

    # ### cupones:
    for c in clientes:
        estado = choices(['Usado', 'No usado'], [0.8, 0.2])
        letras = [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'J',
            'K',
            'L',
            'M',
            'N',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'V',
            'W',
            'X',
            'Y',
            'Z',
        ]
        num = '{:05}'.format(random.randrange(1, 10 ** 8))
        cupon = random.choice(letras) + num + random.choice(letras) + random.choice(letras)
        valor = random.randint(15, 30)
        cup = Cupon(valor, cupon, c.id_cliente, estado[0])
        db.session.add(cup)
    db.session.commit()
    # ###Cargadores

    cargadores = []
    for i in estacioness:
        valor = i.ocupation_actual
        for j in range(32):
            tiposs = ['Carga Normal', 'Carga R\xc3\xa1pida']
            if valor > 0:
                estado = choices(['ocupado', 'libre'], [0.8, 0.2])
                if estado == 'ocupado':
                    valor -= 1
            elif valor == 0:
                estado = 'libre'
            posicion = j
            tipo = random.choice(tiposs)
            sta = i.id_estacion
            carg = Cargador(estado[0], posicion, tipo, sta)
            db.session.add(carg)
            cargadores.append(carg)

    db.session.commit()

    # ### HORAS

    horas = []

    start = datetime(2022, 1, 1)
    end = datetime(2030, 1, 1)

    while start < end:
        a = Horas(start)
        db.session.add(a)
        start = start + relativedelta(minutes=60)
        horas.append(a)

    db.session.commit()

    # ### CONSUMO

    consumos = []
    for c in cargadores:
        cargador = c.id_cargador
        estacion = c.estacion_id
        est = Estacion.query.filter(Estacion.id_estacion == estacion).one_or_none()
        for h in horas:
            hora = h.id
            if h.id < datetime.today():
                potencia_consumida = randint(0, est.potencia_contratada)
                potencia_maxima = est.potencia_contratada

                co1 = Consumo(cargador, hora, potencia_consumida,
                              potencia_maxima)
                db.session.add(co1)
                consumos.append(co1)
            else:
                break

    db.session.commit()

    # ###Modelos

    model_list = [
        '500e Cabrio electrico',
        'Taycan electrico',
        'e-tron GT electrico',
        'Leaf electrico',
        'Ioniq electrico',
        'i3 electrico',
        'ID.3 electrico',
        '2 electrico',
        'UX300e electrico',
        'EV6 electrico',
        ]

    mod = Modelo(model_list[0], 'Fiat', False, 42)
    db.session.add(mod)
    mod2 = Modelo(model_list[1], 'Porsche', True, 93.4)
    db.session.add(mod2)
    mod3 = Modelo(model_list[2], 'Audi', True, 93.4)
    db.session.add(mod3)
    mod4 = Modelo(model_list[3], 'Nissan', False, 42.6)
    db.session.add(mod4)
    mod5 = Modelo(model_list[4], 'Hyundai', False, 72.6)
    db.session.add(mod5)
    mod6 = Modelo(model_list[5], 'BMW', False, 42.2)
    db.session.add(mod6)
    mod7 = Modelo(model_list[6], 'Volkswagen', True, 77)
    db.session.add(mod7)
    mod8 = Modelo(model_list[7], 'Polestar', False, 69)
    db.session.add(mod8)
    mod9 = Modelo(model_list[8], 'Lexus', False, 54.3)
    db.session.add(mod9)
    mod10 = Modelo(model_list[9], 'Kia', True, 77)
    db.session.add(mod10)
    db.session.commit()

    # ###Vehiculos        ####

    vehiculos = []
    modelo = random.choice(model_list)
    vehiculoBueno = Vehiculo("2450GDF", 100, modelo)
    vehiculoBueno2 = Vehiculo("4950KZK", 100, modelo)
    vehiculoBueno3 = Vehiculo("5134FFJ", 100, modelo)
    vehiculoBueno4 = Vehiculo("LU50KZK", 100, modelo)
    db.session.add(vehiculoBueno)
    db.session.add(vehiculoBueno2)
    db.session.add(vehiculoBueno3)
    db.session.add(vehiculoBueno4)
    vehiculos.append(vehiculoBueno)
    vehiculos.append(vehiculoBueno2)
    vehiculos.append(vehiculoBueno3)
    vehiculos.append(vehiculoBueno4)

    for i in range(50):

        letras = ''.join(random.choices(string.ascii_uppercase, k=3))
        numeros = ''.join(random.choices(string.digits, k=4))
        matricula = ''.join(random.choices(letras + numeros, k=7))
        procentaje_bat = random.randint(0, 100)
        modelo = random.choice(model_list)

        v = Vehiculo(matricula, procentaje_bat, modelo)
        db.session.add(v)
        vehiculos.append(v)

    db.session.commit()

    # ### VehiculoCliente

    for i in range(len(clientes) - 1):
        vehiculo = random.choice(vehiculos)
        cliente = clientes[i]

        cliente.vehiculos.append(vehiculo)

    db.session.commit()

    clienteBueno.vehiculos.append(vehiculoBueno)
    clienteBueno.vehiculos.append(vehiculoBueno2)
    clienteBueno.vehiculos.append(vehiculoBueno3)
    clienteBueno.vehiculos.append(vehiculoBueno4)
    db.session.commit()

    # ## RESERVAS
    reservas = []
    for i in range(20):
        id_cargador = random.choice(cargadores).id_cargador
        vehiculo = random.choice(vehiculos)
        c = random.choice(clientes)
        id_cliente = c.id_cliente
        fecha_entrada = fake.date_time_between(start_date='-2y', end_date='now')
        fecha_salida = fake.date_time_between(start_date='-2y', end_date='now')

        procetnaje_carga = randint(vehiculo.procentaje_bat, 100)
        id_vehiculo = vehiculo.matricula
        precio_carga_completa = round(random.uniform(1.0, 100.0), 3)
        precio_carga_actual = round(random.uniform(1.0, 100.0), 3)

        estado = fake.pybool()
        tarifa = round(random.uniform(1.0, 100.0), 3)
        asistida = fake.pybool()
        estado_pago = fake.pybool()
        r1 = Reserva(
            fecha_entrada,
            fecha_salida,
            procetnaje_carga,
            precio_carga_completa,
            precio_carga_actual,
            estado,
            tarifa,
            asistida,
            estado_pago,
            id_cargador,
            id_vehiculo,
            id_cliente,
            )
        db.session.add(r1)
        reservas.append(r1)
        if estado_pago:
            t1 = Transaccion(precio_carga_completa, "Pagado", i, id_cliente)
            c.transacciones.append(t1)
            db.session.add(t1)

    db.session.commit()

    # ### Historial

    for c in clientes:
        veces = random.randint(0, 10)
        for _ in range(veces):
            fecha = fake.date_time_between(start_date='-2y', end_date='now')
            saldo = random.randint(0, 100)
            type = choices(['minus', 'add'], [0.5, 0.5])
            if type == 'minus':
                saldo = saldo * (-1)
                if c.saldo < saldo:
                    type = 'add'
                    saldo = saldo * (-1)
            h1 = Historial(fecha, c.id_cliente, saldo, type[0])
            db.session.add(h1)

    db.session.commit()
