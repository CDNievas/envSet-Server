from flask import Blueprint, request, jsonify
from Mongo import Mongo
from Exceptions import UsuarioNoExisteException, UsuarioYaExisteException
from Tokener import Tokener

apiAuthBP = Blueprint("apiAuthBP", __name__)

@apiAuthBP.route("/")
def login():
    try:

        user = request.values["user"]
        password = request.values["pass"]

        usuario = Mongo.getInstance().login(user,password)

    except UsuarioNoExisteException:
        
        data = {"success":False, "msg":"Usuario inexistente"}
        statusCode = 403
    
    except KeyError:

        data = {"success":False, "msg":"Campos incompletos"}
        statusCode = 400

    else:

        idUsuario = str(usuario["_id"])        
        token = Tokener.getInstance().generarToken(idUsuario)
        data = {"success":True,"msg":"Inicio de sesion correcto. Ya puede utilizar el resto de las funciones.","token":token.decode()}
        statusCode = 200

    return jsonify(data), statusCode


@apiAuthBP.route("/", methods=["POST"])
def register():

    try:
        
        user = request.values["user"]
        password = request.values["pass"]
        Mongo.getInstance().existeUsuario(user)
    
    except KeyError:
        data = {"success":False,"msg":"Campos incompletos"}
        statusCode = 400

    except UsuarioYaExisteException:
        
        data = {"success":False, "msg":"Usuario ya existe"}
        statusCode = 403
    
    else:

        idUsuario = str(Mongo.getInstance().crearUsuario(user,password).inserted_id)     
        token = Tokener.getInstance().generarToken(idUsuario)
        data = {"success":True,"msg":"Usuario registrado correctamente. Ya puede utilizar el resto de las funciones.","token":token.decode()}
        statusCode = 201

    return jsonify(data), statusCode
