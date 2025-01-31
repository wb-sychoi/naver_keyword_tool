from flask import Flask, jsonify, render_template, request
import time
import requests
import os

import signaturehelper

    
def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

# 네이버 API 인증 정보 설정
BASE_URL = os.getenv('BASE_URL', "")
API_KEY = os.getenv('API_KEY', "")
SECRET_KEY = os.getenv('SECRET_KEY', "")
CUSTOMER_ID = os.getenv('CUSTOMER_ID', "")

def chunk_keywords(keywords, chunk_size=5):
    # 쉼표로 구분된 키워드를 리스트로 분리
    keyword_list = keywords.split(',')
    # 5개씩 묶어서 리스트로 반환
    return [keyword_list[i:i + chunk_size] for i in range(0, len(keyword_list), chunk_size)]

def get_data(keywords):
    uri = '/keywordstool'
    method = 'GET'

    response = requests.get(BASE_URL + uri, params={'hintKeywords': keywords,  'showDetail': '1'}, headers=get_header(method,uri,API_KEY,SECRET_KEY,CUSTOMER_ID))

    data = response.json()

    return data


# 전체 데이터 출력 기능
def get_keywords_tool(user_input):
    keyword_chunks = chunk_keywords(user_input)

    all_data = []

    for keyword_chunk in keyword_chunks:
        _keyword = ','.join(keyword_chunk)

        _data = get_data(_keyword)

        all_data.extend(_data['keywordList'])

        time.sleep(2)

    return all_data


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/keyword_data', methods=['POST'])
def keyword_data():
    input_data = request.form.get('keywords', '')

    result_data = get_keywords_tool(input_data)

    return jsonify(result_data)

if __name__ == "__main__":
    app.run(debug=True)