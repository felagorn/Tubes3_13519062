import os
import re
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
import sqlite3
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import and_

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
    katapentingreg = re.findall(x , s.title())
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
    minggu = re.findall('(\\-?[0-9]+ [mM]inggu [kK]e [dD]epan\\b)', s)
    return minggu

def regexNHariKeDepan(s):
    hariN = re.findall('(\\-?[0-9]+ [hH]ari [kK]e [dD]epan\\b)', s)
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

def bmHelp(s):
    return boyerMoore(s.lower(), "help")

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
    fiturHelp = bmHelp(query)

    response = pesanTidakDikenali()
    # Kasus 1: menambahkan jadwal ke database
    if (len(tanggal) == 1) and (len(matkul) == 1) and (len(kataPenting) == 1) and (len(topik) == 1) and (len(taskX) == 0) and (fiturHelp == -1):
        itemid = addJadwal(tanggal[0], matkul[0], kataPenting[0], topik[0])
        if itemid > 0:
            response = ["[TASK BERHASIL DICATAT]", "(ID: " + str(itemid) + ") " + tanggal[0].strftime('%d/%m/%Y') + " - " + matkul[0].upper() + " - " + kataPenting[0].title() + " - " + topik[0]]
    elif (len(tanggal) <= 2) and (len(matkul) == 0) and (len(kataPenting) == 0) and (len(topik) == 0) and (deadline > -1) and (len(taskX) == 0) and (fiturHelp == -1):
        if (len(tanggal) == 0) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 0) and (len(hariIni) == 0):
            deadlines = Jadwal.query.all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
        elif (len(tanggal) == 2) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 0) and (len(hariIni) == 0):
            deadlines = Jadwal.query.filter(Jadwal.tanggal.between(min(tanggal[0], tanggal[1]), max(tanggal[0], tanggal[1]))).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
        elif (len(tanggal) == 0) and (len(nMingguKeDepan) == 1) and (len(nHariKeDepan) == 0) and (len(hariIni) == 0):
            todayDate = datetime.date.today()
            weeks = nMingguKeDepan[0].split(" ")
            deadlines = Jadwal.query.filter(Jadwal.tanggal.between(todayDate, (todayDate + datetime.timedelta(days=1, weeks=int(weeks[0]))))).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
        elif (len(tanggal) == 0) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 1) and (len(hariIni) == 0):
            todayDate = datetime.date.today()
            days = nHariKeDepan[0].split(" ")
            deadlines = Jadwal.query.filter(Jadwal.tanggal.between(todayDate, (todayDate + datetime.timedelta(days=(int(days[0]) + 1))))).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
        elif (len(tanggal) == 0) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 0) and (len(hariIni) == 1):
            todayDate = datetime.date.today()
            tomorrowDate = todayDate + datetime.timedelta(days=1)
            deadlines = Jadwal.query.filter(Jadwal.tanggal.between(todayDate, tomorrowDate)).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
    elif (len(tanggal) <= 2) and (len(matkul) == 0) and (len(kataPenting) == 1) and (len(topik) == 0) and (deadline >= -1) and (len(taskX) == 0) and (fiturHelp == -1):
        if (len(tanggal) == 0) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 0) and (len(hariIni) == 0):
            deadlines = Jadwal.query.filter_by(jenis_tugas=kataPenting[0].title()).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
        elif (len(tanggal) == 2) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 0) and (len(hariIni) == 0):
            deadlines = Jadwal.query.filter(and_(Jadwal.tanggal.between(min(tanggal[0], tanggal[1]), max(tanggal[0], tanggal[1])), (Jadwal.jenis_tugas == kataPenting[0].title()))).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
        elif (len(tanggal) == 0) and (len(nMingguKeDepan) == 1) and (len(nHariKeDepan) == 0) and (len(hariIni) == 0):
            todayDate = datetime.date.today()
            weeks = nMingguKeDepan[0].split(" ")
            deadlines = Jadwal.query.filter(and_(Jadwal.tanggal.between(todayDate, (todayDate + datetime.timedelta(days=1, weeks=int(weeks[0])))), (Jadwal.jenis_tugas == kataPenting[0].title()))).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
        elif (len(tanggal) == 0) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 1) and (len(hariIni) == 0):
            todayDate = datetime.date.today()
            days = nHariKeDepan[0].split(" ")
            deadlines = Jadwal.query.filter(and_(Jadwal.tanggal.between(todayDate, (todayDate + datetime.timedelta(days=(int(days[0]) + 1)))), (Jadwal.jenis_tugas == kataPenting[0].title()))).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
        elif (len(tanggal) == 0) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 0) and (len(hariIni) == 1):
            todayDate = datetime.date.today()
            tomorrowDate = todayDate + datetime.timedelta(days=1)
            deadlines = Jadwal.query.filter(and_(Jadwal.tanggal.between(todayDate, tomorrowDate), (Jadwal.jenis_tugas == kataPenting[0].title()))).all()
            if len(deadlines) == 0:
                response = ["Tidak ada"]
            else:
                response = ["[Daftar Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(str(i) + ". (ID: " + str(dl.id) + ") " + dl.tanggal.strftime('%d/%m/%Y') + " - " + dl.matkul + " - " + dl.jenis_tugas + " - " + dl.topik_tugas)
                    i += 1
    elif(len(matkul)==1) and (deadline>-1) and (len(kataPenting)==1) and (fiturHelp == -1):
        deadlines = Jadwal.query.filter(and_(Jadwal.matkul==matkul[0].upper(), Jadwal.jenis_tugas == kataPenting[0].title())).all()    
        if(kataPenting[0].title() != "Tucil" and kataPenting[0].title() !="Tubes"):
            response = ["Bukan deadline kak :("]
        else:
            if deadlines:
                response = ["[Daftar Tanggal Deadline]"]
                i = 1
                for dl in deadlines:
                    response.append(dl.tanggal.strftime('%d/%m/%Y'))
                    i += 1
            else:
                response = ["Yey, gaada deadline"]
        #KASUS 4 = UPDATE TANGGAL (kata kunci = tanggal dan task X)
    elif (len(tanggal) == 1) and (len(taskX)==1) and (fiturHelp == -1):
        taskList = taskX[0].split(" ")
        idDelete = int(taskList[1])
        update_tanggal = Jadwal.query.filter(Jadwal.id == idDelete).first()
        if update_tanggal: 
            update_tanggal.tanggal = tanggal[0]
            db.session.commit()
            response = ["[TASK BERHASIL DIUPDATE]"]
        else: 
            response = ["[TASK TIDAK ADA TOLONG CEK KEMBALI]"]
    #KASUS 5 = HAPUS TANGGAL (kata kunci = task X dan selesai)
    elif (len(tanggal) == 0) and (len(taskX)==1) and (selesai>-1) and (fiturHelp == -1):
        taskList = taskX[0].split(" ")
        idDelete = int(taskList[1])
        delete_jadwal = Jadwal.query.filter(Jadwal.id == idDelete).first()
        if delete_jadwal:
            db.session.delete(delete_jadwal)
            db.session.commit()
            response = ["[TASK BERHASIL DIHAPUS]"]
        else:
            response = ["[TASK TIDAK ADA TOLONG CEK KEMBALI]"]
    elif ((persona > -1) or (fitur > -1) or (fiturHelp > -1)) and (len(tanggal) == 0) and (len(kataPenting) == 0) and (len(matkul) == 0) and (len(topik) == 0) and (deadline == -1) and (len(nMingguKeDepan) == 0) and (len(nHariKeDepan) == 0) and (len(hariIni) == 0) and (len(taskX) == 0) and (selesai == -1):
        response = ["[Fitur]"]
        with open(os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), "static/fitur.txt"), "r", encoding="utf-8") as fiturFile:
            for line in fiturFile:
                response.append(line)
        response.append("[Daftar kata penting]")
        with open(os.path.join(app.config["UPLOAD_PATH"], "katapenting.txt"), "r") as kataPentingFile:
            kataPentingIdx = 1
            for line in kataPentingFile:
                response.append(str(kataPentingIdx) + ". " + line)
                kataPentingIdx += 1

    return render_template("chat.html", query=query, response=response)