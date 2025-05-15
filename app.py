from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import sqlite3
import pandas as pd
import json
import urllib.request
from selenium import webdriver
# Selenium 옵션 및 서비스 추가
from selenium.webdriver.chrome.options import Options as ChromeOptions
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

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # 헤드리스 모드 필수!
    chrome_options.add_argument("--no-sandbox") # 서버 환경에서 자주 필요
    chrome_options.add_argument("--disable-dev-shm-usage") # /dev/shm 리소스 문제 방지
    chrome_options.add_argument("--disable-gpu") # 헤드리스 모드에서는 GPU 가속 불필요
    chrome_options.add_argument("window-size=1920x1080") # 가상 윈도우 크기 설정

    driver = None # driver 변수 초기화

    try:
        # chromedriver가 시스템 PATH에 설정되어 있다고 가정합니다.
        # 만약 특정 경로에 chromedriver를 두었다면, Service 객체를 사용해야 합니다.
        # from selenium.webdriver.chrome.service import Service as ChromeService
        # chromedriver_path = "/usr/local/bin/chromedriver" # 서버의 chromedriver 경로 예시
        # service = ChromeService(executable_path=chromedriver_path)
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)

    except Exception as e:
        app.logger.error(f"Error initializing ChromeDriver: {e}")
        # 사용자에게 오류 메시지를 보여주거나, 오류 페이지로 리다이렉트 할 수 있습니다.
        return f"크롬 드라이버 초기화 중 오류 발생: {e}. 서버 관리자에게 문의하거나 서버 로그를 확인하세요."

    if driver is None:
        # 드라이버 초기화에 실패한 경우 처리
        return "크롬 드라이버를 시작할 수 없습니다. 서버 설정을 확인해주세요."

    # 크롤링 시작
    try:
        driver.get('https://github.com/sujinbang')
        screenshot_filename = 'github_page_loaded.png'
        driver.save_screenshot(os.path.join(app.static_folder, screenshot_filename)) # static 폴더에 저장
        time.sleep(3) # 페이지 로딩 대기 (더 나은 방법은 WebDriverWait 사용)

        # 메뉴 파싱
        html = driver.page_source
        soup = bs(html, "html.parser")

        # 요소 선택 시, 해당 요소가 없을 경우를 대비하여 방어 코드 추가
        h1_element = soup.select_one('div.markdown-heading') # select_one 사용
        h1 = h1_element.text.strip() if h1_element else "H1 제목 없음"

        h1_body_element = soup.select_one('.markdown-body p')
        h1_body = h1_body_element.text.strip() if h1_body_element else "H1 본문 없음"

        h2_element = soup.select_one('h2.heading-element')
        h2 = h2_element.text.strip() if h2_element else "H2 제목 없음"
        
        li_list = []
        li_elements = soup.select('.markdown-body li')
        for i in range(min(5, len(li_elements))): # IndexError 방지
            li_list.append(li_elements[i].text.strip())

    except Exception as e:
        app.logger.error(f"크롤링 중 오류 발생: {e}")
        return f"데이터를 가져오는 중 오류가 발생했습니다: {e}"
    finally:
        if driver:
            driver.quit() # 브라우저와 드라이버 세션 종료 (close() 대신 quit() 권장)
    
    return render_template('webData/selenium_result.html', h1=h1, h1_body=h1_body, h2=h2, li_lists=li_list, screenshot_filename=screenshot_filename)

# 실행파일 다운로드
@app.route("/download_exe")
def download_exe():
    return send_file("data/unlockSApp.exe", mimetype='application/octet-stream', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)