# coding=UTF-8
from flask import Flask
from flask.sessions import NullSession
from flask.templating import render_template
from pymongo import MongoClient
from flask_pymongo import PyMongo
from tabulate import tabulate
import pandas as pd
from flask import request
from waitress import serve

app = Flask(__name__)


# password = getpass.getpass("Introduce tu contrasseña de MongoDB por favor:  ")
client = MongoClient("URL de mongodb")
db = client["pruebadb"]
collection = db['clientes']


# client["pruebadb"]["clientes"].insert_one({"nombre": "Eduardo", "apellido": "Rojas"})
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    cursor = collection.find({})
    tabla=""
    df = pd.DataFrame(list(cursor))
    del df['_id']
    df = df.to_html()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        client["pruebadb"]["clientes"].insert_one({"nombre": nombre, "apellido": apellido})
    return render_template("menu.html", tabla=tabla, df=df)

@app.route("/reg", methods=['GET', 'POST'])
def registrar():
    collection = db['usuarios']
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        pasw = request.form['psw']
        correo = request.form['correo']
        client["pruebadb"]["usuarios"].insert_one({"nombre": nombre, "apellido": apellido, "correo": correo, "contraseña": pasw})
    return render_template("reg.html")
#serve(app, host='0.0.0.0', port="80")
#app.run(host="0.0.0.0", port='80')
