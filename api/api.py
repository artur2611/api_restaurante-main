from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from config import config
from models import db, Usuario, Ejercicio, Sesion
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import jwt
import datetime
import os

def create_app(environment):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(environment)
    db.init_app(app)
    if app.config.get("DEBUG"):
        with app.app_context():
            db.create_all()

    return app
env_name = os.environ.get("FLASK_ENV", "development")
environment = config[env_name]
app = create_app(environment)


def error_response(message, code=400):
    return jsonify({"error": message}), code


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        
        auth_header = request.headers.get('Authorization', None)
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        elif 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return error_response("A valid token is missing", 401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Usuario.query.filter_by(id=data['id']).first()
            if current_user is None:
                return error_response("Usuario no existe", 401)
        except jwt.ExpiredSignatureError:
            return error_response("Token expired", 401)
        except jwt.InvalidTokenError:
            return error_response("Token is invalid", 401)
        except Exception as e:
            return error_response(f"Token error: {str(e)}", 401)

        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/registro', methods=['POST'])
def register():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    telefono = data.get('telefono')
    fecha_nacimiento = data.get('fecha_nacimiento')  
    rol = data.get('rol', 'paciente')
    contrasena = data.get('contrasena')

    if not nombre or not contrasena:
        return error_response("Nombre y contrasena son requeridos", 400)

    if telefono and Usuario.query.filter_by(telefono=telefono).first():
        return error_response("Telefono ya registrado", 400)
    new_user = Usuario(
        
        id=str(uuid.uuid4()),
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        telefono=telefono,
        rol=rol,
        # contrasena=contrasena_hash,
        
    )
    if contrasena and contrasena.strip():
        new_user.contrasena = generate_password_hash(contrasena)
    else:
        return error_response("Contraseña inválida", 400)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado correctamente", "usuario": new_user.json()}), 201


@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    #print("HOLA")
    auth = request.authorization
    print("##############auth",auth)   
    

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    user = Usuario.query.filter_by(nombre=auth.username).first()

    if not user:
        return make_response('Usuario no existe', 401)

    if check_password_hash(user.contrasena, auth.password):
        token = jwt.encode(
            {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({'token': token, 'id': user.id})

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/usuarios', methods=['GET'])
@token_required
def listar_usuarios(current_user):
    usuarios = [u.json() for u in Usuario.query.all()]
    return jsonify({"usuarios": usuarios}), 200

@app.route('/usuarios/<string:user_id>', methods=['GET'])
@token_required
def get_usuario(current_user, user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return error_response("Usuario no encontrado", 404)
    return jsonify({"usuario": usuario.json()}), 200

@app.route('/usuarios', methods=['POST'])
def crear_usuario_public():
    
    return register()

@app.route('/usuarios/<string:user_id>', methods=['PUT'])
@token_required
def update_usuario(current_user, user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return error_response("Usuario no encontrado", 404)
    data = request.get_json() or {}
    usuario.nombre = data.get('nombre', usuario.nombre)
    if data.get('fecha_nacimiento'):
        usuario.fecha_nacimiento = data.get('fecha_nacimiento')
    usuario.telefono = data.get('telefono', usuario.telefono)
    usuario.rol = data.get('rol', usuario.rol)
    print(data)
    if data.get('contrasena'):
        usuario.contrasena = generate_password_hash(data.get('contrasena'))
    db.session.commit()
    return jsonify({"message": "Usuario actualizado", "usuario": usuario.json()}), 200

@app.route('/usuarios/<string:user_id>', methods=['DELETE'])
@token_required
def delete_usuario(current_user, user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return error_response("Usuario no encontrado", 404)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200


@app.route('/ejercicios', methods=['GET'])
@token_required
def listar_ejercicios(current_user):
    ejercicios = [e.json() for e in Ejercicio.query.all()]
    return jsonify({"ejercicios": ejercicios}), 200

@app.route('/ejercicios/<string:ej_id>', methods=['GET'])
@token_required
def get_ejercicio(current_user, ej_id):
    ejercicio = Ejercicio.query.get(ej_id)
    if not ejercicio:
        return error_response("Ejercicio no encontrado", 404)
    return jsonify({"ejercicio": ejercicio.json()}), 200

@app.route('/ejercicios', methods=['POST'])
@token_required
def crear_ejercicio(current_user):
    data = request.get_json() or {}
    numero = data.get('numero_ejercicio')
    descripcion = data.get('descripcion')
    repeticiones_base = data.get('repeticiones_base')
    dificultad = data.get('dificultad')

    if not (numero and descripcion and repeticiones_base and dificultad):
        return error_response("Faltan campos requeridos", 400)

    if Ejercicio.query.filter_by(numero_ejercicio=numero).first():
        return error_response("Numero de ejercicio ya existe", 400)

    e = Ejercicio(
        #probare el id ya que no se autogenera devido a que es varchar para probar la creacion de ejercicios
        id=str(uuid.uuid4()),
        numero_ejercicio=numero,
        descripcion=descripcion,
        repeticiones_base=repeticiones_base,
        dificultad=dificultad
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({"message": "Ejercicio creado", "ejercicio": e.json()}), 201

@app.route('/ejercicios/<string:ej_id>', methods=['PUT'])
@token_required
def update_ejercicio(current_user, ej_id):
    ejercicio = Ejercicio.query.get(ej_id)
    if not ejercicio:
        return error_response("Ejercicio no encontrado", 404)
    data = request.get_json() or {}
    ejercicio.numero_ejercicio = data.get('numero_ejercicio', ejercicio.numero_ejercicio)
    ejercicio.descripcion = data.get('descripcion', ejercicio.descripcion)
    ejercicio.repeticiones_base = data.get('repeticiones_base', ejercicio.repeticiones_base)
    ejercicio.dificultad = data.get('dificultad', ejercicio.dificultad)
    db.session.commit()
    return jsonify({"message": "Ejercicio actualizado", "ejercicio": ejercicio.json()}), 200

@app.route('/ejercicios/<string:ej_id>', methods=['DELETE'])
@token_required
def delete_ejercicio(current_user, ej_id):
    ejercicio = Ejercicio.query.get(ej_id)
    if not ejercicio:
        return error_response("Ejercicio no encontrado", 404)
    db.session.delete(ejercicio)
    db.session.commit()
    return jsonify({"message": "Ejercicio eliminado"}), 200


@app.route('/sesiones', methods=['GET'])
@token_required
def listar_sesiones(current_user):
    """
    Devuelve las sesiones incluyendo los datos del usuario (nombre, id, ...) y
    del ejercicio asociado en cada sesión.
    """
    sesiones = []
    for s in Sesion.query.all():
        usuario = Usuario.query.get(s.id_usuario)
        ejercicio = Ejercicio.query.get(s.id_ejercicio)

        ses = s.json()
        ses['usuario'] = usuario.json() if usuario else None
        ses['ejercicio'] = ejercicio.json() if ejercicio else None

        sesiones.append(ses)

    return jsonify({"sesiones": sesiones}), 200




@app.route('/sesiones/<string:s_id>', methods=['GET'])
@token_required
def get_sesion(current_user, s_id):
    s = Sesion.query.get(s_id)
    if not s:
        return error_response("Sesion no encontrada", 404)
    return jsonify({"sesion": s.json()}), 200

@app.route('/sesiones', methods=['POST'])
@token_required
def crear_sesion(current_user):
    data = request.get_json() or {}
    id_ejercicio = data.get('id_ejercicio')
    id_usuario = data.get('id_usuario')
    repeticiones_logradas = data.get('repeticiones_logradas')
    maximo_nivel_logrado = data.get('maximo_nivel_logrado')

    if not (id_ejercicio and id_usuario and repeticiones_logradas is not None):
        return error_response("Faltan campos requeridos", 400)

    if not Ejercicio.query.get(id_ejercicio):
        return error_response("Ejercicio no existe", 404)
    if not Usuario.query.get(id_usuario):
        return error_response("Usuario no existe", 404)

    s = Sesion(
        id=str(uuid.uuid4()),
        id_ejercicio=id_ejercicio,
        id_usuario=id_usuario,
        repeticiones_logradas=repeticiones_logradas,
        maximo_nivel_logrado=maximo_nivel_logrado
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({"message": "Sesion creada", "sesion": s.json()}), 201

@app.route('/sesiones/<s_id>', methods=['PUT'])
@token_required
def update_sesion(current_user, s_id):
    s = Sesion.query.get(s_id)
    if not s:
        return error_response("Sesion no encontrada", 404)
    data = request.get_json() or {}
    if data.get('id_ejercicio') and not Ejercicio.query.get(data.get('id_ejercicio')):
        return error_response("Ejercicio no existe", 404)
    if data.get('id_usuario') and not Usuario.query.get(data.get('id_usuario')):
        return error_response("Usuario no existe", 404)

    s.id_ejercicio = data.get('id_ejercicio', s.id_ejercicio)
    s.id_usuario = data.get('id_usuario', s.id_usuario)
    s.repeticiones_logradas = data.get('repeticiones_logradas', s.repeticiones_logradas)
    s.maximo_nivel_logrado = data.get('maximo_nivel_logrado', s.maximo_nivel_logrado)
    s.fecha_termino = data.get('fecha_termino', s.fecha_termino)
    
    # generacion de fecha_termino si se cumplen las condiciones
    ejercicio = Ejercicio.query.get(s.id_ejercicio)
    repeticiones_base = getattr(ejercicio, 'repeticiones_base', 0)
    
    if s.repeticiones_logradas >= repeticiones_base and repeticiones_base > 0:
        s.fecha_termino = datetime.datetime.now()
    
    db.session.commit()
    return jsonify({"message": "Sesion actualizada", "sesion": s.json()}), 200

@app.route('/sesiones/<string:s_id>', methods=['DELETE'])
@token_required
def delete_sesion(current_user, s_id):
    s = Sesion.query.get(s_id)
    if not s:
        return error_response("Sesion no encontrada", 404)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": "Sesion eliminada"}), 200

@app.route('/sesiones/usuario/<string:user_id>', methods=['GET'])
@token_required
def listar_sesiones_por_usuario(current_user, user_id):
    """
    Devuelve las sesiones pendientes de un usuario específico incluyendo datos
    del usuario y del ejercicio asociado en cada sesión. No restringe por rol,
    solo requiere un token válido. Se incluyen únicamente sesiones sin
    fecha_termino.
    """
    #print("USER ID EN LA API:", user_id)
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return error_response("Usuario no encontrado", 404)

    sesiones = []
    for s in Sesion.query.filter_by(id_usuario=user_id).filter(Sesion.fecha_termino.is_(None)).all():
        ejercicio = Ejercicio.query.get(s.id_ejercicio)

        ses = s.json()
        ses['usuario'] = usuario.json()
        ses['ejercicio'] = ejercicio.json() if ejercicio else None
        sesiones.append(ses)
    #print("SESION CON DATOS COMPLETOS:", sesiones)

    return jsonify({"sesiones": sesiones}), 200


if __name__ == '__main__':
    app.run(debug=True)
