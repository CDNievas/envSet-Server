# SO
import os, datetime

from Exceptions import TokenIncorrectoException

import jwt

class Tokener():

    __instance = None
    secretKey = None

    @staticmethod
    def getInstance():
        if Tokener.__instance == None:
            Tokener()
        return Tokener.__instance

    def generarToken(self, idUsuario):

        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
                "iat": datetime.datetime.utcnow(),
                "sub": idUsuario
            }
            return jwt.encode(
                payload,
                self.secretKey,
                algorithm="HS256"
            )
            
        except Exception as e:
            print(e)


    def validarToken(self, token):
        try:
            payload = jwt.decode(token, self.secretKey)
            return payload["sub"]

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise TokenIncorrectoException

    def __init__(self):
        if Tokener.__instance != None:
            raise Exception("Singleton class")
        else:
            Tokener.__instance = self
            self.secretKey = os.urandom(24)