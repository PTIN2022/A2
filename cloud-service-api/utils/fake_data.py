import string
import random
from faker import Faker
from models.model import *
from datetime import datetime

def fakedata():
        fake = Faker()
        ####Estaciones####
        e = Estacion("VG1", 41.217606, 1.727072, 32, "Rambla de L'exposicio",20,"Zona industrial", 1,130, "+34762487248", "Vilanova i la geltru", "España")  # , t.id_trabajador
        db.session.add(e)
        e2 = Estacion("VG2", 41.221002, 1.730369, 32, "Rambla de A",20,"Zona mayonesa", 15,130,"+34762854712", "Vilanova i la geltru", "España")  # , t.id_trabajador
        db.session.add(e2)
        e3 = Estacion("VG3", 41.225431, 1.7337627, 32, "A veces",20,"Zona M de motomami", 8,130, "+34785123478", "Vilanova i la geltru", "España")  # , t.id_trabajador
        db.session.add(e3)
        e4 = Estacion("VG4", 41.227420, 1.728166, 32, "Rambla de Shrek",20,"Zona memes de baki", 1,130, "+34745821523", "Vilanova i la geltru", "España")  # , t.id_trabajador
        db.session.add(e4)
        e5 = Estacion("VG5", 41.229674, 1.721478, 32, "Casoplon del coletas",20,"Zona SEAX", 14,130, "+34797458744", "Vilanova i la geltru", "España")  # , t.id_trabajador
        db.session.add(e5)
        e6 = Estacion("VG6", 41.222119, 1.718915, 32, "Casa de ibai",20,"Zona el bicho", 20,130, "+34768220011", "Vilanova i la geltru", "España")  # , t.id_trabajador
        db.session.add(e6)
        e7 = Estacion("VG7", 41.223434, 1.710113, 32, "Rambla de Redes Multimedia",20,"Zona XAMU", 26,130, "+34798544552", "Vilanova i la geltru", "España")  # , t.id_trabajador
        db.session.add(e7)
        e8 = Estacion("VG8", 41.217122, 1.709477, 32, "Bar pepin",20,"Zona vip", 32,130, "+34768855471", "Vilanova i la geltru", "España")  # , t.id_trabajador
        db.session.add(e8)
        db.session.commit()
        estacioness = [e,e2,e3,e4,e5,e6,e7,e8]


#         c = Cliente("sergi", "garcia", "meh@gmail.com","245363Y", "foto_chula", 4674387249, "sergi.ib", "mehmeh123")
#         db.session.add(c)
#         db.session.commit()

#         t = Trabajador("sergi", "garcia", "meh@gmail.com","24536FT", "foto_chula", 4674387249, "sergi.ib", "mehmeh123", "jefe", "Activo", datetime.today(), "Amigo de la infancia?", e.id_estacion)
#         db.session.add(t)
#         db.session.commit()

#         #e.encargado = t.id_trabajador
#         #db.session.commit()


#         p = Promociones(32, 2, datetime.today(), datetime.today(), "activa", "superdescuento")
#         p.estaciones.append(e)
#         db.session.add(p)
#         db.session.commit()

        ####Cargadores####
        for i in estacioness:
            for j in range(32):
                estadoss = ["ocupado","libre"]
                tiposs = ["Carga Normal","Carga Rápida"]
                estado = random.choice(estadoss)
                posicion = j
                tipo = random.choice(tiposs)
                sta = i.id_estacion
                carg = Cargador(estado,posicion,tipo,sta)
                db.session.add(carg)
        db.session.commit()

#         p1 = Cargador("ocupado", 2, "tipo C", e.id_estacion)
#         p2 = Cargador("libre", 5, "super fast", e.id_estacion)
#         db.session.add(p1)
#         db.session.add(p2)
#         db.session.commit()

#         h1 = Horas(datetime.today())  # , p1.id_cargador
#         h2 = Horas(datetime.today())  # , p2.id_cargador
#         db.session.add(h1)
#         db.session.add(h2)
#         db.session.commit()

#         co1 = Consumo(p1.id_cargador, h1.id, 50, 100)
#         co2 = Consumo(p2.id_cargador, h2.id, 70, 90)
#         db.session.add(co1)
#         db.session.add(co2)
#         db.session.commit()
        
#         ####Modelos####
#         model_list = ["500e Cabrio eléctrico", "Taycan eléctrico","e-tron GT eléctrico", "Leaf eléctrico", "Ioniq eléctrico", "i3 eléctrico", "ID.3 eléctrico", "2 eléctrico", "UX300e eléctrico", "EV6 eléctrico"]
        
#         mod = Modelo(model_list[0], "Fiat", False, 42)
#         db.session.add(mod)
#         mod2 = Modelo(model_list[1], "Porsche", True, 93.4)
#         db.session.add(mod2)
#         mod3 = Modelo(model_list[2], "Audi", True, 93.4)
#         db.session.add(mod3)
#         mod4 = Modelo(model_list[3], "Nissan", False, 42.6)
#         db.session.add(mod4)
#         mod5 = Modelo(model_list[4], "Hyundai", False, 72.6)
#         db.session.add(mod5)
#         mod6 = Modelo(model_list[5], "BMW", False, 42.2)
#         db.session.add(mod6)
#         mod7 = Modelo(model_list[6], "Volkswagen", True, 77)
#         db.session.add(mod7)
#         mod8 = Modelo(model_list[7], "Polestar", False, 69)
#         db.session.add(mod8)
#         mod9 = Modelo(model_list[8], "Lexus", False, 54.3)
#         db.session.add(mod9)
#         mod10 = Modelo(model_list[9], "Kia", True, 77)
#         db.session.add(mod10)
#         db.session.commit()

#         ####Vehiculos####
#         for i in range(50):

#             letras = ''.join(random.choices(string.ascii_uppercase, k=3))
#             numeros = ''.join(random.choices(string.digits, k=4))
#             matricula = ''.join(random.choices(letras+numeros, k=7))
#             procentaje_bat = random.randint(0, 100)
#             modelo = random.choice(model_list)

#             v = Vehiculo(matricula, procentaje_bat, modelo)
#             db.session.add(v)

#         #v = Vehiculo("X96392WXES", 34, mod.modelo)
#         #db.session.add(v)
#         db.session.commit()
#         #### ???? ####
#         c.vehiculos.append(v)
#         db.session.commit()

#         r1 = Reserva(datetime.today(), datetime.today(), 50, 25.2,10.1, True, 90.99, True,True,p1.id_cargador, v.matricula, c.id_cliente)
#         r2 = Reserva(datetime.today(), datetime.today(), 33, 50, 60,
#                      False, 44.44, True,True,p2.id_cargador, v.matricula, c.id_cliente)
#         db.session.add(r1)
#         db.session.add(r2)
#         db.session.commit()

#         a = Aviso("Cancelación","motomamiiiiii",datetime.today(), r1.id_reserva, c.id_cliente)#c.id_cliente
#         db.session.add(a)
#         db.session.commit()

#         ticket = Ticket(datetime.today(), "Error App",
#                         "No me deja reservar en la estacion de Rambla Exposicio, no se que le pasa", "Pendiente", c.id_cliente)
#         db.session.add(ticket)
#         db.session.commit()

#         m = Mensaje("Me parece que lo haceis todo mal, salu2",datetime.today(), c.id_cliente, ticket.id_ticket)
#         db.session.add(m)
#         db.session.commit()

#         av = Averia(datetime.today(), "Pendiente",
#                         "No funciona la estación por mantenimiento", t.id_trabajador, e.id_estacion)
#         db.session.add(av)
#         db.session.commit()

#         s = Sesiones(datetime.today(), datetime.today(), t.id_trabajador)
#         db.session.add(s)
#         db.session.commit()
#         ####CLiente####
#         for i in range(50):
#             l = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
#              'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
#             num = '{:08}'.format(random.randrange(1, 10**8))
#             nombre = fake.first_name()
#             apellido = fake.last_name()
#             email = fake.free_email()
#             dni = num + random.choice(l)
#             foto = fake.name()
#             telefono = '{:09}'.format(random.randrange(1, 10**8))
#             username = nombre + num
#             password = apellido + num

#             usuario_te = Cliente(nombre, apellido, email, dni, foto, telefono, username, password)
#             db.session.add(usuario_te)
#             db.session.commit()
        

# ####Trabajador####
#         for i in range(10):
#             l = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
#              'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
#             num = '{:08}'.format(random.randrange(1, 10**8))
#             nombre = fake.first_name()
#             apellido = fake.last_name()
#             email = fake.free_email()
#             dni = num + random.choice(l)
#             foto = fake.name()
#             telefono = '{:09}'.format(random.randrange(1, 10**8))
#             username = nombre + num
#             password = apellido + num
#             cargos = ['administrador','encargado','trabajador']
#             estados = ['Activo','Inactivo']
#             cargo = random.choice(cargos)
#             estado = random.choice(estados)
#             estacion = random.choice(estacioness)

#             tr = Trabajador(nombre, apellido, email, dni, foto, telefono, username, password, cargo, estado, datetime.today(), "Amigo de la infancia?", estacion.id_estacion)
#             db.session.add(tr)
#             db.session.commit()
