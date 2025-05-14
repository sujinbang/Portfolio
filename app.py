from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import sqlite3
import pandas as pd
import json
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import sys
import os
import time

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

# 이력서 다운로드
@app.route("/download")
def download_resume():
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

# 크롤링 - 네이버 API 활용
@app.route('/webdata1')
def naver_API():
    return render_template('webData/naver_api.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']  # input name 속성으로 접근

    client_id = "hGm9TuroERHaloW0EJIM"
    client_secret = "n9kINNNSc2"
    # query = "차량 진단 기술"
    # query = input("검색할 단어를 입력하세요 : ")
    encText = urllib.parse.quote(user_input)
    display = 10  # 한 번에 가져올 결과 수

    all_results = []

    for i in range(10):
        start = i * 100 + 1  # 각 요청의 시작 인덱스 설정
        url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={display}&start={start}"
        naver_request = urllib.request.Request(url)
        naver_request.add_header("X-Naver-Client-Id", client_id)
        naver_request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(naver_request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body.decode('utf-8'))
            all_results.extend(results['items'])  # 검색 결과 추가
        else:
            print(f"Error Code: {rescode}")
            break

    # 결과를 데이터프레임으로 변환
    data = {
        "title": [result["title"] for result in all_results],
        "link": [result["link"] for result in all_results],
        # "description": [result["description"] for result in all_results],
        "pubDate": [result["pubDate"] for result in all_results],
        # "originallink": [result["originallink"] for result in all_results]
    }

    df = pd.DataFrame(data)
    # 'n.news.naver.com'이 포함된 링크만 필터링
    filtered_df = df[df['link'].str.contains('n.news.naver.com')].copy()

    # 링크를 실제 하이퍼링크로 바꾸기 (선택)
    filtered_df['link'] = filtered_df['link'].apply(lambda x: f"<a href='{x}' target='_blank'>{x}</a>")

    return render_template('webData/naver_api_result.html', table=filtered_df.to_html(escape=False, index=False))

# 크롤링 - Selenium 활용
@app.route('/webdata2')
def selenium():
    return render_template('webData/selenium.html')

@app.route('/selenium')
def selenium_result():

    if getattr(sys, 'frozen', False) and hasattr(sys, "_MEIPASS"):
        driver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome()

    # 크롤링 시작
    driver.get('https://github.com/sujinbang')
    time.sleep(3)

    # 메뉴 파싱
    html = driver.page_source
    soup = bs(html, "html.parser")

    h1 = soup.select('div.markdown-heading')[0].text
    h1_body = soup.select('.markdown-body p')[0].text
    h2 = soup.select('h2.heading-element')[0].text
    li_list = []

    for i in range(0, 5):
        li_list.append( soup.select('.markdown-body li')[i].text )


    driver.close()

    return render_template('webData/selenium_result.html', h1=h1, h1_body=h1_body, h2=h2, li_lists=li_list)

# 실행파일 다운로드
@app.route("/download_exe")
def download_exe():
    return send_file("data/unlockSApp.exe", mimetype='application/octet-stream', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=8080)