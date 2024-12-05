from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)

# Allow CORS
CORS(app)

@app.route('/api/hello', methods=['GET'])
def hello_world():
    response = {
        "message": "Hello, World!",
        "status": "success"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)