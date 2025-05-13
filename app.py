from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
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

@app.route("/download")
def download_test():
    return send_file("data/resume.pdf", mimetype="application/pdf", as_attachment=True)

# 부산 관광 현황
@app.route('/Festival')
def Festival():
    return render_template('busan/Festival.html')
@app.route('/Food')
def Food():
    return render_template('busan/Food.html')
@app.route('/Market')
def Market():
    return render_template('busan/Market.html')
@app.route('/Ocean')
def Ocean():
    return render_template('busan/Ocean.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)