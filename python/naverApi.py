import os
import sys
import urllib.request
import json
import csv
import pandas as pd

client_id = "hGm9TuroERHaloW0EJIM"
client_secret = "n9kINNNSc2"
query = "차량 진단 기술"
# query = input("검색할 단어를 입력하세요 : ")
encText = urllib.parse.quote(query)
display = 10  # 한 번에 가져올 결과 수

all_results = []

for i in range(10):
    start = i * 100 + 1  # 각 요청의 시작 인덱스 설정
    url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={display}&start={start}"
    print(url)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
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
    "description": [result["description"] for result in all_results],
    "pubDate": [result["pubDate"] for result in all_results],
    "originallink": [result["originallink"] for result in all_results]
}
df = pd.DataFrame(data)
# 'n.news.naver.com'이 포함된 링크만 필터링
filtered_df = df[df['link'].str.contains('n.news.naver.com')].copy()
# df = pd.read_csv('naver_search_results_차량진단기술.csv', encoding='utf-8')
filtered_df