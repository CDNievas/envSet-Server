from pymongo import MongoClient
from bson.objectid import ObjectId

from Exceptions import UsuarioNoExisteException, UsuarioYaExisteException

class Mongo():

    __instance = None
    client = None
    db = None

    @staticmethod
    def getInstance():
        if Mongo.__instance == None:
            Mongo()
        return Mongo.__instance

    def login(self, username, password):

        query = {"username": username, "password":password}
        usuario = self.db.usuarios.find_one(query)

        if(usuario != None):
            return usuario
        else:
            raise UsuarioNoExisteException
    
    def existeUsuario(self, username):

        query = {"username": username}
        usuario = self.db.usuarios.find_one(query)

        if(usuario != None):
            raise UsuarioYaExisteException

    def crearUsuario(self, username, password):

        query = {"username": username, "password":password, "envs":[]}
        return self.db.usuarios.insert_one(query)

    def setEnv(self, idUsuario, name, value, desc):

        query = {"_id": ObjectId(idUsuario)}
        usuario = self.db.usuarios.find_one(query)
        
        if(usuario != None):

            env = {"name": name, "value": value, "desc":desc}
            usuario["envs"].append(env)

            usuario["envs"] = [env for env in usuario["envs"] if env["name"] != name]
            usuario["envs"].append(env)

            self.db.usuarios.replace_one(query, usuario)

        else:
            raise UsuarioNoExisteException

    def getEnv(self, idUsuario, envName):

        query = {"_id": ObjectId(idUsuario)}
        usuario = self.db.usuarios.find_one(query)
    
        if(usuario != None):
            
            if(envName != None):
                
                envFound = None
                for env in usuario["envs"]:
                    if(env["name"] == envName):
                        envFound = env
                        break
                
                if(envFound != None):
                    return {"success":True,"value":envFound["value"]}
                else:
                    return {"success":False,"msg":"Esa variable no existe"}
            
            else: 

                envs = []
                for env in usuario["envs"]:
                    envs.append({"name":env["name"],"desc":env["desc"]})
                return {"success":True,"envs":envs}

        else:
            raise UsuarioNoExisteException

    def __init__(self, _url=None):
        if Mongo.__instance != None:
            raise Exception("Singleton class")
        else:
            Mongo.__instance = self
            self.client = MongoClient(_url)
            self.db = self.client.env