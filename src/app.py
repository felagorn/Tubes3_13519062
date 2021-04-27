import re
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
import sqlite3

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "../test"