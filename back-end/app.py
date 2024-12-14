import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from AhoCorasickSearch import AhoCorasick
from NegationDetector import NegationDetector
from LongestSeqSearch import LongestNonOverlappingIntervals
from HpoFactory import HpoFactory
from HpoLookup import HpoLookup
from GptSearch import GptSearch
from ScispacySearch import ScispacySearch
from OardClient import OardClient
from Phen2geneClient import Phen2geneClient

app = Flask(__name__)

# Allow CORS
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for verbose output
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

logger = logging.getLogger(__name__)  # Create a logger for this module

# Initialize HPO Factory
logger.info("Initializing HPO Factory...")
hpo_F = HpoFactory()
hpo_tree = hpo_F.build_hpo_tree()
hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
hpo_dict, hpo_name_dict, _ = hpo_F.build_hpo_dict(hpo_ancestors)
hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)

# Initialize Aho-Corasick
logger.info("Initializing Aho-Corasick...")
try:
    ac = AhoCorasick(hpo_dict)
except Exception as e:
    logger.exception("Error initializing Aho-Corasick")
    raise e

# Initialize Scispacy
logger.info("Initializing Scispacy...")
try:
    ss = ScispacySearch()
except Exception as e:
    logger.exception("Error initializing Scispacy")
    raise e

# Initialize OardClient
logger.info("Initializing OardClient...")
try:
    oard_client = OardClient()
except Exception as e:
    logger.exception("Error initializing OardClient")
    raise e

# Initialize Phen2geneClient
logger.info("Initializing Phen2geneClient...")
try:
    phen2gene_client = Phen2geneClient()
except Exception as e:
    logger.exception("Error initializing Phen2geneClient")
    raise e

@app.route('/api/hello', methods=['GET'])
def hello_world():
    logger.debug("Received request for /api/hello")
    import time
    time.sleep(10)
    response = {
        "message": "Hello, World!",
        "status": "success"
    }
    logger.debug("Responding to /api/hello with success message")
    return jsonify(response)

# Custom error handler for all exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    status_code = 500
    if hasattr(e, 'code'):  # For HTTP exceptions
        status_code = e.code
    response = {
        "error": str(e),
        "type": type(e).__name__,
        "status": status_code
    }
    logger.error(f"Exception occurred: {response}")
    return jsonify(response), status_code

@app.route('/api/search/actree', methods=['POST'])
def search_actree():
    logger.debug("Received request for /api/search/actree")
    try:
        request_data = request.get_json()
        text = request_data.get("text")
        logger.info(f"Processing text for actree: {text}")
        intervals = ac.search(text)
        detector = NegationDetector(negation_window=10, sentence_delimiters=None)
        intervals = [m for m in intervals if not detector.is_negated(text, m)]
        selector = LongestNonOverlappingIntervals(intervals)
        intervals = selector.get_longest_intervals()
        matched_hpo = HpoLookup.add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels, None)
        matches = HpoLookup.add_hpo_frequency(matched_hpo, oard_client)
        logger.info("Successfully processed actree search")
        return jsonify(matches), 200
    except Exception as e:
        logger.exception("Error in /api/search/actree")
        raise e

@app.route('/api/search/gpt', methods=['POST'])
def search_gpt():
    logger.debug("Received request for /api/search/gpt")
    try:
        request_data = request.get_json()
        text = request_data.get("text")
        api_key = request_data.get("openaiKey")
        test = request_data.get("test")
        logger.info(f"Processing GPT search with text: {text}")
        gpt = GptSearch(openai_api_key=api_key)
        gpt_response = gpt.search_hpo_terms(text, test=test)
        intervals, gpt_response_hpo_terms = gpt.post_process_gpts(gpt_response)
        detector = NegationDetector(negation_window=10, sentence_delimiters=None)
        intervals = [m for m in intervals if not detector.is_negated(text, m)]
        selector = LongestNonOverlappingIntervals(intervals)
        longest_intervals = selector.get_longest_intervals()
        matching_indices = [i for i, a in enumerate(longest_intervals) if a in intervals]
        gpt_response_hpo_terms = [gpt_response_hpo_terms[i] for i in matching_indices]
        matched_hpo = HpoLookup.add_hpo_attributes(text, longest_intervals, hpo_dict, hpo_name_dict, hpo_levels, gpt_response_hpo_terms)   
        matches = HpoLookup.add_hpo_frequency(matched_hpo, oard_client)
        logger.info("Successfully processed GPT search")
        return jsonify(matches), 200
    except Exception as e:
        logger.exception("Error in /api/search/gpt")
        raise e

@app.route('/api/search/scispacy', methods=['POST'])
def search_scispacy():
    logger.debug("Received request for /api/search/scispacy")
    try:
        request_data = request.get_json()
        text = request_data.get("text")
        logger.info(f"Processing Scispacy search with text: {text}")
        intervals, linked_hpo_names = ss.search(text)
        detector = NegationDetector(negation_window=10, sentence_delimiters=None)
        intervals = [m for m in intervals if not detector.is_negated(text, m)]
        selector = LongestNonOverlappingIntervals(intervals)
        longest_intervals = selector.get_longest_intervals()
        matching_indices = [i for i, a in enumerate(longest_intervals) if a in intervals]
        linked_hpo_names = [linked_hpo_names[i] for i in matching_indices]
        matched_hpo = HpoLookup.add_hpo_attributes(text, longest_intervals, hpo_dict, hpo_name_dict, hpo_levels, linked_hpo_names)
        matches = HpoLookup.add_hpo_frequency(matched_hpo, oard_client)
        logger.info("Successfully processed Scispacy search")
        return jsonify(matches), 200
    except Exception as e:
        logger.exception("Error in /api/search/scispacy")
        raise e

@app.route('/api/predictgene', methods=['POST'])
def predict_gene():
    logger.debug("Received request for /api/predictgene")
    try:
        request_data = request.get_json()
        highlights = request_data.get("highlights")
        include_low_priority = request_data.get("includeLowPriority")
        include_predicted_gene = request_data.get("includePredictedGene")
        rank = request_data.get("rank")
        threshold = request_data.get("threshold")
        logger.info(f"Processing predict gene with highlights: {highlights}")
        if include_low_priority:
            hpo_ids = [h["hpoAttributes"]["id"] for h in highlights if "id" in h["hpoAttributes"]]
        else:
            hpo_ids = [h["hpoAttributes"]["id"] for h in highlights if "id" in h["hpoAttributes"] and h["priority"] == "Normal"]
        hpo_ids = list(set([h for h in hpo_ids if h is not None]))
        genes = phen2gene_client.get_genes(hpo_ids)
        if include_predicted_gene:
            status = None
        else:
            status = "SeedGene"
        filtered_genes = phen2gene_client.filter_results(genes, rank=int(rank), score=float(threshold), status=status)
        logger.info("Successfully processed predict gene")
        return jsonify(filtered_genes), 200
    except Exception as e:
        logger.exception("Error in /api/predictgene")
        raise e

if __name__ == "__main__":
    logger.info("Starting the Flask application...")
    app.run(debug=True)
