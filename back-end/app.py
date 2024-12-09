from flask import Flask, jsonify, request
from flask_cors import CORS
from AhoCorasickSearch import AhoCorasick
from NegationDetector import NegationDetector
from LongestSeqSearch import LongestNonOverlappingIntervals
from HpoFactory import HpoFactory
from HpoLookup import HpoLookup
from GptSearch import GptSearch
from ScispacySearch import ScispacySearch



app = Flask(__name__)

# Allow CORS
CORS(app)

# Initialize HPO Factory
hpo_F = HpoFactory()
hpo_tree = hpo_F.build_hpo_tree()
hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
hpo_dict, hpo_name_dict = hpo_F.build_hpo_dict(hpo_ancestors)
hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)

# Initialize Aho-Corasick
ac = AhoCorasick(hpo_dict)

# Initialize Scispacy
ss = ScispacySearch()

@app.route('/api/hello', methods=['GET'])
def hello_world():
    # sleep 10 seconds
    import time
    time.sleep(10)
    response = {
        "message": "Hello, World!",
        "status": "success"
    }
    return jsonify(response)

@app.route('/api/search/actree', methods=['POST'])
def search_actree():
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
    matches = HpoLookup.add_hpo_attributes(text, intervals,hpo_dict, hpo_name_dict,hpo_levels)
    return jsonify(matches)

@app.route('/api/search/gpt', methods=['POST'])
def search_gpt():
    request_data = request.get_json()
    text = request_data.get("text")
    api_key = request_data.get("openaiKey")
    test = request_data.get("test")
    gpt = GptSearch(openai_api_key = api_key)
    gpt_response = gpt.search_hpo_terms(text, test=test)
    intervals, gpt_response_hpo_terms = gpt.post_process_gpts(gpt_response)
    detector = NegationDetector(negation_window=10, sentence_delimiters=None)
    intervals = [m for m in intervals if not detector.is_negated(text, m)]
    # post-process to return non-overlapping ones
    selector = LongestNonOverlappingIntervals(intervals)
    longest_intervals = selector.get_longest_intervals()
    # Find matching indices
    matching_indices = [i for i, a in enumerate(longest_intervals) if a in intervals]
    gpt_response_hpo_terms = [gpt_response_hpo_terms[i] for i in matching_indices]
    matched_hpo = HpoLookup.add_hpo_attributes(text, longest_intervals, hpo_dict, hpo_name_dict, hpo_levels, gpt_response_hpo_terms)    
    return jsonify(matched_hpo)

@app.route('/api/search/scispacy', methods=['POST'])
def search_scispacy():
    request_data = request.get_json()
    text = request_data.get("text")
    intervals, linked_hpo_names = ss.search(text)
    detector = NegationDetector(negation_window=10, sentence_delimiters=None)
    intervals = [m for m in intervals if not detector.is_negated(text, m)]
    # post-process to return non-overlapping ones
    selector = LongestNonOverlappingIntervals(intervals)
    longest_intervals = selector.get_longest_intervals()
    # Find matching indices
    matching_indices = [i for i, a in enumerate(longest_intervals) if a in intervals]
    linked_hpo_names = [linked_hpo_names[i] for i in matching_indices]
    matched_hpo = HpoLookup.add_hpo_attributes(text, longest_intervals, hpo_dict, hpo_name_dict, hpo_levels, linked_hpo_names)
    return jsonify(matched_hpo)

if __name__ == "__main__":
    app.run(debug=True)