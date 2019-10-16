
# SO
import os

# WebApp
from flask import Flask
from bp import *
from webBP import webBP

# MongoDB
from Mongo import Mongo

#PORT = os.environ.get("PORT")
#MONGODB = os.environ.get("MONGODB")

PORT = 8080
MONGODB = "localhost:27017"

app = Flask(__name__)

if __name__ == "__main__":

    mongo = Mongo(MONGODB)
    app.secret_key = os.urandom(12)
    app.register_blueprint(webBP)
    app.register_blueprint(apiAuthBP, url_prefix="/api/auth")
    app.register_blueprint(apiEnvBP, url_prefix="/api/envs")
    app.run("0.0.0.0",PORT,debug=True)

