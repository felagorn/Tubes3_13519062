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
        tanggal.append(t[0])
    return tanggal

def regexKataPenting(s):
    katapenting = []
    with open(os.path.join(app.config["UPLOAD_PATH"], "katapenting.txt"), "r") as filekata:
        for line in filekata:
            katapenting.append(line.rstrip())
    x = '(\\b'+'|'.join(katapenting)+'\\b)'
    katapentingreg = re.findall(x , s)
    print(katapentingreg)

def regexMatkul(s):
    matkul = re.findall('(\\b[a-zA-Z][a-zA-Z]\\d{4}\\b)', s)
    print(matkul)

def regexDeadline(s):
    deadline = re.findall('(\\b[dD]eadline\\b)', s)
    print(deadline)

def regexMinggu(s):
    minggu = re.findall('(\\b[0-9]+ [mM]inggu [kK]e [dD]epan\\b)', s)
    print(minggu)

def regexHariN(s):
    hariN = re.findall('(\\b[0-9]+ [hH]ari [kK]e [dD]epan\\b)', s)
    print(hariN)

def regexHariIni(s):
    hariIni = re.findall('(\\b[hH]ari [iI]ni\\b)', s)
    print(hariIni)

def regexTaskX(s):
    taskX = re.findall('(\\b[tT]ask [0-9]+\\b)', s)
    print(taskX)

def regexSelesai(s):
    selesai = re.findall('(\\b[sS]elesai\\b)', s)
    print(selesai)

def regexPersona(s):
    persona = re.findall('(\\b[pP]ersona\\b)', s)
    print(persona)

def regexFitur(s):
    fitur = re.findall('(\\b[fF]itur\\b)', s)
    print(fitur)

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "../test"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.config["UPLOAD_PATH"], "jadwal.db")
db = SQLAlchemy(app)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def chat():
    query = request.args.get("q")
    print(query)
    tanggal = regexTanggal(query)
    print(tanggal)
    return render_template("chat.html", query=query)