# Web
from flask import Blueprint, request, jsonify

from Tokener import Tokener
from Mongo import Mongo

from Exceptions import TokenIncorrectoException, UsuarioNoExisteException

apiEnvBP = Blueprint("apiEnvBP", __name__)

@apiEnvBP.route("/", defaults={'envName': None})
@apiEnvBP.route("/<envName>")
def getEnv(envName):

    try:
        idUsuario = getUser(request)
        data = Mongo.getInstance().getEnv(idUsuario,envName)
        statusCode = 200

    except TokenIncorrectoException:
        data = {"success":False,"msg":"Token auth incorrecto. Intenta iniciando sesion nuevamente"}
        statusCode = 401

    except IndexError:
        data = {"success":False,"msg":"No existe ese id"}
        statusCode = 400

    return jsonify(data), statusCode

@apiEnvBP.route("/", methods=["POST"])
def setEnv():

    try:
        
        idUsuario = getUser(request)

        name = request.values["name"]
        value = request.values["value"]
        desc = request.values["desc"]

        Mongo.getInstance().setEnv(idUsuario, name, value, desc)

        data = {"success":True,"msg":"Variable guardada correctamente"}
        statusCode = 201

    except UsuarioNoExisteException: 
        data = {"success":False,"msg":"Usuario inexistente"}
        statusCode = 403

    except TokenIncorrectoException:
        data = {"success":False,"msg":"Token auth incorrecto. Intenta iniciando sesion nuevamente"}
        statusCode = 401

    except KeyError:
        data = {"success":False,"msg":"Campos incompletos"}
        statusCode = 400

    return jsonify(data), statusCode

# Check auth function
def getUser(request):
    try:
        authToken = request.headers["Authorization"]
        return Tokener.getInstance().validarToken(authToken)
    except KeyError:
        raise TokenIncorrectoException
