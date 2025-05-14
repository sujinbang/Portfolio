from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import sys
import os
import time

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