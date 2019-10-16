# Web
from flask import Blueprint, request, flash, jsonify

from Tokener import Tokener
from Mongo import Mongo

from Exceptions import TokenIncorrectoException, UsuarioNoExisteException

apiEnvBP = Blueprint("apiBP", __name__)

@apiEnvBP.route("/", defaults={'idEnv': None})
@apiEnvBP.route("/<idEnv>")
def getEnv(idEnv):

    try:
        idUsuario = getUser(request)
        data = Mongo.getInstance().getEnv(idUsuario,idEnv)
        statusCode = 200

    except TokenIncorrectoException:
        data = {"success":False,"error":"Token auth incorrecto. Intenta iniciando sesion nuevamente"}
        statusCode = 401

    except IndexError:
        data = {"success":False,"error":"No existe ese id"}
        statusCode = 400

    return data, statusCode

@apiEnvBP.route("/", methods=["POST"])
def setEnv():

    try:
        
        idUsuario = getUser(request)
        print(idUsuario)

        name = request.values["name"]
        value = request.values["value"]
        
        Mongo.getInstance().setEnv(idUsuario, name, value)

        data = {"success":True}
        statusCode = 201

    except UsuarioNoExisteException: 
        data = {"success":False,"error":"Usuario inexistente"}
        statusCode = 403

    except TokenIncorrectoException:
        data = {"success":False,"error":"Token auth incorrecto. Intenta iniciando sesion nuevamente"}
        statusCode = 401

    except KeyError:
        data = {"success":False,"error":"Campos incompletos"}
        statusCode = 400

    return data, statusCode

# Check auth function
def getUser(request):
    try:
        authToken = request.headers["Authorization"].split(" ")[1]
        return Tokener.getInstance().validarToken(authToken)
    except KeyError:
        raise TokenIncorrectoException
