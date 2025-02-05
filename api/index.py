from flask import Flask, jsonify, render_template, request

from index import get_keywords_tool


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/keyword_data', methods=['POST'])
def keyword_data():
    input_data = request.form.get('keywords', '')

    result_data = get_keywords_tool(input_data)

    return jsonify(result_data)
