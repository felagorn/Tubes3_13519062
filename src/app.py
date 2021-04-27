import re
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
import sqlite3

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
