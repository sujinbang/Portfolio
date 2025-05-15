from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import os
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import sys


# def selenium_result():

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
    print(f"Error initializing ChromeDriver: {e}")


if driver is None:
    # 드라이버 초기화에 실패한 경우 처리
    print("크롬 드라이버를 시작할 수 없습니다. 서버 설정을 확인해주세요.")

# 크롤링 시작
try:
    driver.get('https://github.com/sujinbang')
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
    print(f"크롤링 중 오류 발생: {e}")
finally:
    if driver:
        driver.quit() # 브라우저와 드라이버 세션 종료 (close() 대신 quit() 권장)

print(h1,h1_body,h2,li_list)

    # return render_template('webData/selenium_result.html', h1=h1, h1_body=h1_body, h2=h2, li_lists=li_list)