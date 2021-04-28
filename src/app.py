import os
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

def regextanggal(s):
    tanggals = re.findall('(\\b\\d{2}/([1-9]|1[0-2]|0[1-9])/\\d{4}\\b)', s)
    tanggal =[]
    for t in tanggals: 
        tanggal.append(t[0])
    print(tanggal)

def regexkatapenting(s):
    katapenting = []
    with open(os.path.join(app.config["UPLOAD_PATH"], "katapenting.txt"), "r") as filekata:
        for line in filekata: 
            katapenting.append(line.rstrip())
    x = '(\\b'+'|'.join(katapenting)+'\\b)'
    katapentingreg = re.findall(x , s)
    print(katapentingreg)

def regexmatkul(s):
    matkul = re.findall('(\\b[a-zA-Z][a-zA-Z]\\d{4}\\b)', s)
    print(matkul)

def regexdeadline(s):
    deadline = re.findall('(\\b[dD]eadline\\b)', s)
    print(deadline)

def regexminggu(s):
    minggu = re.findall('(\\b[0-9]+ [mM]inggu [kK]e [dD]epan\\b)', s)
    print(minggu)

def regexhariN(s):
    hariN = re.findall('(\\b[0-9]+ [hH]ari [kK]e [dD]epan\\b)', s)
    print(hariN)

def regexhariIni(s):
    hariIni = re.findall('(\\b[hH]ari [iI]ni\\b)', s)
    print(hariIni)

def regexTaskX(s):
    taskX = re.findall('(\\b[tT]ask [0-9]+\\b)', s)
    print(taskX)

def regexselesai(s):
    selesai = re.findall('(\\b[sS]elesai\\b)', s)
    print(selesai)

def regexpersona(s):
    persona = re.findall('(\\b[pP]ersona\\b)', s)
    print(persona)

def regexfitur(s):
    fitur = re.findall('(\\b[fF]itur\\b)', s)
    print(fitur)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def query():
    query = request.args.get("q")
    print(query)
    regexTaskX(query)
    regexselesai(query)
    regexpersona(query)
    regexfitur(query)
    return render_template("chat.html")


