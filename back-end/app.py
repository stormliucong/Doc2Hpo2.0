from flask import Flask, jsonify, request
from flask_cors import CORS

from AhoCorasickSearch import AhoCorasick
from NegationDetector import NegationDetector
from LongestSeqSearch import LongestNonOverlappingIntervals
from HpoDict import HpoDict


app = Flask(__name__)

# Allow CORS
CORS(app)

# Initialize Aho-Corasick
hpo_dict = HpoDict("hpo_file.txt").build_hpo_dict()
ac = AhoCorasick(hpo_dict)


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
    intervals = ac.search(text) # Example: [(1, 4), (2, 4), (2, 6)]
    # post-process to return non-negated ones
    detector = NegationDetector(negation_window=10, sentence_delimiters=None)
    intervals = [m for m in intervals if not detector.is_negated(text, m)]
    # post-process to return non-overlapping ones
    selector = LongestNonOverlappingIntervals(intervals)
    intervals = selector.get_longest_intervals()
    # add hpo atrributes
    matches = ac.add_hpo_attributes(text, intervals,hpo_dict)
    print(matches)
    return jsonify(matches)

if __name__ == "__main__":
    app.run(debug=True)