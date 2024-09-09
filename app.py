from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Load the summarization model
summarizer = pipeline("summarization")

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Text Summarization API'})

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()

    text = data.get('text', '')

    if len(text) > 0:
        if len(text) > 3000:  
            chunks = [text[i:i + 3000] for i in range(0, len(text), 3000)]
            summary = ''
            for chunk in chunks:
                summary += summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text'] + ' '
        else:
            summary = summarizer(text, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'No text provided'}), 400

    



if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=4300)
