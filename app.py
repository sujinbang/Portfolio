from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import pandas as pd
import json

app = Flask(__name__)

# SQLite DB 파일 경로
DB_PATH = 'database.db'

def get_db_connection():
    """SQLite3 DB 연결하는 함수"""
    conn = sqlite3.connect(DB_PATH)
    return conn

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/data/seoul.geojson')
def serve_geojson():
    return send_from_directory('data', 'seoul.geojson')

@app.route('/echarts')
def echart():

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)