from flask import Blueprint, jsonify

apiPingBP = Blueprint("apiPingBP", __name__)

@apiPingBP.route("/")
def ping():

    data = {"success":True,"msg":"Pong!"}
    statusCode = 200

    return jsonify(data), statusCode