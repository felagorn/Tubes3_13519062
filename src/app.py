import re
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
import sqlite3
import datetime

def sqlConnect(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except sqlite3.Error as e:
        print(str(e))
    return connection

def sqlUpdate(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except sqlite3.Error as e:
        print(str(e))

def sqlSelect(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(str(e))
    return result

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "../test"

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/query", methods=["GET"])
def query():
    query = request.args.get("q")
    print(query)
    return render_template("index.html")
