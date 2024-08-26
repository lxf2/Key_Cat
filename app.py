# app.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def find_text_containing_keyword(url, keyword):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            text_nodes = soup.find_all(text=True)
            count = 0
            results = []
            
            for text in text_nodes:
                if keyword in text:
                    results.append(text.strip())
                    count += text.count(keyword)
            
            return {"results": results, "count": count}
        else:
            return {"error": f"请求失败，状态码：{response.status_code}"}
    except Exception as e:
        return {"error": f"发生错误：{e}"}

@app.route('/search', methods=['POST'])
def search():
    url = request.json.get('url')
    keyword = request.json.get('keyword')
    return jsonify(find_text_containing_keyword(url, keyword))

if __name__ == '__main__':
    app.run(debug=True)