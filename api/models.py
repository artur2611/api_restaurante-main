from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(15), unique=True, nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)

    sesiones = db.relationship("Sesion", backref="usuario", cascade="all, delete-orphan")

    def json(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_nacimiento": str(self.fecha_nacimiento),
            "telefono": self.telefono,
            "rol": self.rol,
            "contrasena" : self.contrasena
        }



class Ejercicio(db.Model):
    __tablename__ = "ejercicios"
    #pruebas que quisas no sirvan
    #id = db.Column(db.Integer, primary_key=True) cambiamos a string ya que cambiamos el formato de la id por un varchar 
    id = db.Column(db.String(200), primary_key=True)
    numero_ejercicio = db.Column(db.Integer, unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    repeticiones_base = db.Column(db.Integer, nullable=False)
    dificultad = db.Column(db.String(20), nullable=False)
    #no me carga los datos en la bse estoy revisando si el tipo de dato es el correcto
    #fecha_creacion = db.Column(db.DateTime) la libreria func.now() jala machin pa la fecha padrinos
    fecha_creacion = db.Column(db.DateTime, server_default=func.now())



    sesiones = db.relationship("Sesion", backref="ejercicio", cascade="all, delete-orphan")

    def json(self):
        return {
            "id": self.id,
            "numero_ejercicio": self.numero_ejercicio,
            "descripcion": self.descripcion,
            "repeticiones_base": self.repeticiones_base,
            "dificultad": self.dificultad,
            "fecha_creacion": str(self.fecha_creacion)
        }



class Sesion(db.Model):
    __tablename__ = "sesion"

    id = db.Column(db.String(200), primary_key=True)
    fecha_creado = db.Column(db.DateTime, server_default=func.now())
    
    id_ejercicio = db.Column(db.String(200), db.ForeignKey("ejercicios.id"), nullable=False)
    id_usuario = db.Column(db.String(200), db.ForeignKey("usuarios.id"), nullable=False)

    repeticiones_logradas = db.Column(db.Integer, nullable=False)
    maximo_nivel_logrado = db.Column(db.String(50))

    def json(self):
        return {
            "id": self.id,
            "fecha_creado": str(self.fecha_creado),
            "id_ejercicio": self.id_ejercicio,
            "id_usuario": self.id_usuario,
            "repeticiones_logradas": self.repeticiones_logradas,
            "maximo_nivel_logrado": self.maximo_nivel_logrado
        }
