import nltk
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.word_processor import get_word_data

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    word = data.get('word', '').strip()

    if not word:
        return jsonify({'valid': False, 'error': 'No word provided'}), 400

    try:
        result = get_word_data(word)
        return jsonify(result)
    except nltk.corpus.reader.wordnet.WordNetError as wn_err:
        print(f"WordNet error: {str(wn_err)}")
        return jsonify({'valid': False, 'error': 'WordNet lookup failed', 'details': str(wn_err)}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'valid': False, 'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)