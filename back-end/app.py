from flask import Flask, jsonify, request
from flask_cors import CORS
from AhoCorasickSearch import AhoCorasick 



app = Flask(__name__)

# Allow CORS
CORS(app)

# Initialize Aho-Corasick
terms = ["he", "she", "his", "hers"]
ac = AhoCorasick(terms)


@app.route('/api/hello', methods=['GET'])
def hello_world():
    response = {
        "message": "Hello, World!",
        "status": "success"
    }
    return jsonify(response)

@app.route('/api/search/actree', methods=['POST'])
def search():
    request_data = request.get_json()
    text = request_data.get("text")
    matches = ac.search(text)
    return jsonify(matches)

if __name__ == "__main__":
    app.run(debug=True)