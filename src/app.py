import os
import re
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
import sqlite3
import datetime
from flask_sqlalchemy import SQLAlchemy

def findFails(pattern):
    fails = []
    fails.append(0)
    i = 1
    j = 0
    while i < len(pattern):
        if pattern[j] == pattern[i]:
            fails.append(j + 1)
            i += 1
            j += 1
        elif j > 0:
            j = fails[j - 1]
        else:
            fails.append(0)
            i += 1
    return fails

def knuthMorrisPratt(string, pattern):
    fails = findFails(pattern)
    i = 0
    j = 0
    while (i < len(string)):
        if string[i] == pattern[j]:
            if j == (len(pattern) - 1):
                return i - len(pattern) + 1
            i += 1
            j += 1
        elif j > 0:
            j = fails[j - 1]
        else:
            i += 1
    return -1

def findLastOccurence(pattern):
    lastOccurence = {}
    for i in range(len(pattern)):
        lastOccurence[pattern[i]] = i
    return lastOccurence

def boyerMoore(string, pattern):
    lastOccurence = findLastOccurence(pattern)
    i = len(pattern) - 1
    if i > (len(string) - 1):
        return -1
    j = len(pattern) - 1
    do = True
    while do or (i <= (len(string) - 1)):
        if string[i] == pattern[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            if string[i] in lastOccurence:
                i = i + len(pattern) - min(j , (1 + lastOccurence[string[i]]))
                j = len(pattern) - 1
            else:
                i = i + len(pattern) - min(j , 0)
                j = len(pattern) - 1
        if do:
            do = False
    return -1

def regexTanggal(s):
    tanggals = re.findall('(\\b\\d{2}/([1-9]|1[0-2]|0[1-9])/\\d{4}\\b)', s)
    tanggal =[]
    for t in tanggals: 
        td = datetime.datetime.strptime(t[0], "%d/%m/%Y")
        tanggal.append(td)
    return tanggal

def regexKataPenting(s):
    katapenting = []
    with open(os.path.join(app.config["UPLOAD_PATH"], "katapenting.txt"), "r") as filekata:
        for line in filekata:
            katapenting.append(line.rstrip())
    x = '(\\b'+'|'.join(katapenting)+'\\b)'
    katapentingreg = re.findall(x , s)
    return katapentingreg

def regexMatkul(s):
    matkul = re.findall('(\\b[a-zA-Z][a-zA-Z]\\d{4}\\b)', s)
    return matkul

def regexTopik(s):
    topik = re.findall(r'"(.+?)"', s)
    return topik
    
def kmpDeadline(s):
    return knuthMorrisPratt(s.lower(), "deadline")

def regexNMingguKeDepan(s):
    minggu = re.findall('(\\b[0-9]+ [mM]inggu [kK]e [dD]epan\\b)', s)
    return minggu

def regexNHariKeDepan(s):
    hariN = re.findall('(\\b[0-9]+ [hH]ari [kK]e [dD]epan\\b)', s)
    return hariN

def regexHariIni(s):
    hariIni = re.findall('(\\b[hH]ari [iI]ni\\b)', s)
    return hariIni

def regexTaskX(s):
    taskX = re.findall('(\\b[tT]ask [0-9]+\\b)', s)
    return taskX

def kmpSelesai(s):
    return knuthMorrisPratt(s.lower(), "selesai")

def bmPersona(s):
    return boyerMoore(s.lower(), "persona")

def bmFitur(s):
    return boyerMoore(s.lower(), "fitur")

def pesanTidakDikenali():
    return ["Maaf, pesan tidak dikenali"]

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "../test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(app.config["UPLOAD_PATH"], "jadwal.db")
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Jadwal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, nullable = False)
    matkul = db.Column(db.String(255), nullable = False)
    jenis_tugas = db.Column(db.String(255), nullable = False)
    topik_tugas = db.Column(db.String(255), nullable = False)

def addJadwal(tanggal, matkul, jenis_tugas, topik_tugas):
    jadwal = Jadwal(tanggal=tanggal, matkul=matkul.upper(), jenis_tugas=jenis_tugas.title(), topik_tugas=topik_tugas)
    db.session.add(jadwal)
    db.session.flush()
    db.session.commit()
    return jadwal.id

@app.route("/")
@app.route("/index")
def index():
    rows = Jadwal.query.all()
    for row in rows:
        print(str(row.id) + " " + str(row.tanggal) + " " + str(row.matkul) + " " + str(row.jenis_tugas) + " " + str(row.topik_tugas))
    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def chat():
    query = request.args.get("q")
    
    # lakukan semua pengecekan string
    tanggal = regexTanggal(query)
    kataPenting = regexKataPenting(query)
    matkul = regexMatkul(query)
    topik = regexTopik(query)
    deadline = kmpDeadline(query)
    nMingguKeDepan = regexNMingguKeDepan(query)
    nHariKeDepan = regexNHariKeDepan(query)
    hariIni = regexHariIni(query)
    taskX = regexTaskX(query)
    selesai = kmpSelesai(query)
    persona = bmPersona(query)
    fitur = bmFitur(query)

    response = pesanTidakDikenali()
    # Kasus 1: menambahkan jadwal ke database
    if (len(tanggal) == 1) and (len(matkul) == 1) and (len(kataPenting) == 1) and (len(topik) == 1) and (taskX is None):
        itemid = addJadwal(tanggal[0], matkul[0], kataPenting[0], topik[0])
        if itemid > 0:
            response = ["[TASK BERHASIL DICATAT]", "(ID: " + str(itemid) + ") " + tanggal[0].strftime('%d/%m/%Y') + " - " + matkul[0] + " - " + kataPenting[0] + " - " + topik[0]]
        else:
            response = pesanTidakDikenali()
    elif (tanggal is None) and (matkul is None) and (kataPenting is None) and (topik is None) and (deadline > -1):
        if (nMingguKeDepan is None) and (nHariKeDepan is None) and (hariIni is None) and (taskX is None):
            print()

    return render_template("chat.html", query=query, response=response)