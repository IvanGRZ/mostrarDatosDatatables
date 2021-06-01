import os
from flask import Flask, render_template, request, json , redirect, request, current_app, url_for, flash
from flask_mysqldb import MySQL,MySQLdb #se utilizo para las consultas flaks_mysqldb
import mysql.connector
import csv
import io
from datetime import datetime

app = Flask(__name__)

app.secret_key = "caircocoders-ednalan-2020"

#conexion a la base de datos con flaskmysqldb
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'prueba'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql2 = MySQL(app)

#se hace la consulta a la base de datos y con fetchall devuelve todas las filas
@app.route("/", methods=['POST','GET'])
def index():
    cur = mysql2.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM proyectos")
    rows = cur.fetchall()
    return render_template('index.html', rows=rows)

#creacion de la tabla en la base de datos (codigo que dio el profe)
@app.route('/upload', methods =['POST'])
def upload():

    content = request.files['inputfile']
    stream = io.StringIO(content.stream.read().decode("ANSI"), newline = None)
    reader = csv.reader(stream)
    columnas = next(reader)

    sql = "create table if not exists proyectos (id1 INTEGER AUTO_INCREMENT PRIMARY KEY, "
    sql = sql + (" varchar(150), ".join(columnas)+ " varchar(150))")
    print(sql)

    mydb = mysql.connector.connect(host="localhost",database="prueba",user="root",password="12345")
    cursor= mydb.cursor()
    cursor.execute(sql)
    mydb.commit()
    print("Tabla creada!")

    for fila in reader:
        cursor.execute("insert into proyectos values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", fila)
    mydb.commit()
    mydb.close()
    print("Proceso terminado!")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()