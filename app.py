# SO
import os

# WebApp
from flask import Flask
from bp import *
from webBP import webBP

# MongoDB
from Mongo import Mongo

PORT = os.environ.get("ENVSETPORT")
MONGODB = os.environ.get("ENVSETDB")

app = Flask(__name__)

mongo = Mongo(MONGODB)
app.secret_key = os.urandom(12)
app.register_blueprint(webBP)
app.register_blueprint(apiPingBP, url_prefix="/api/ping")
app.register_blueprint(apiAuthBP, url_prefix="/api/auth")
app.register_blueprint(apiEnvBP, url_prefix="/api/envs")
app.run("0.0.0.0",PORT,debug=False)

