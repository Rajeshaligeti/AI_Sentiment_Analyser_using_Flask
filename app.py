from flask import Flask, render_template, request, jsonify
from flask import send_from_directory
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import re
import chardet

# Initialize Flask app
app = Flask(__name__)

# Load sentiment model
def load_sentiment_model():
    return OllamaLLM(model="llama3.2")  # Replace with actual model if necessary

sentiment_model = load_sentiment_model()

# Preprocess function
def preprocess_input(text):
    if not text.strip() or re.match(r'^[0-9a-fA-F]+$', text.strip()):
        return None
    return text

# Parse sentiment and confidence from the model response
def parse_sentiment_response(response):
    try:
        if not response.strip():
            return {"sentiment": "Neutral", "confidence": 0.5}
        match = re.search(r"Sentiment:\s*(\w+).?Confidence\s*Score?:?\s([\d.]+)", response, re.DOTALL)
        if match:
            sentiment = match.group(1).strip().capitalize()
            confidence = float(match.group(2).strip())
            return {"sentiment": sentiment, "confidence": confidence}
        return {"sentiment": "Neutral", "confidence": 0.5}
    except Exception:
        return {"sentiment": "Neutral", "confidence": 0.5}

# Analyze sentiment for a single input
def analyze_sentiment(text):
    preprocessed_text = preprocess_input(text)
    if not preprocessed_text:
        return None
    template = (
        "You are an AI sentiment analyzer that interprets all types of inputs, including informal, rude, or slang language. "
        "Please return the sentiment (positive, negative, neutral, or mixed) and a confidence score (0 to 1), regardless of the input.\n"
        "Input: {input_text}\nResponse:"
    )
    prompt = ChatPromptTemplate.from_template(template)
    prompt_value = prompt.format(input_text=preprocessed_text)
    response = sentiment_model.invoke(prompt_value)
    return parse_sentiment_response(response)

# Detect file encoding
def detect_encoding(file):
    raw_data = file.read(10000)
    result = chardet.detect(raw_data)
    file.seek(0)
    return result['encoding']

def generate_wordcloud(text):
    wordcloud = WordCloud(background_color="white").generate(text)
    wordcloud_path = os.path.join('static', 'wordcloud.png')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(wordcloud_path, format='png')
    plt.close()
    return wordcloud_path


# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    sentiment, confidence = None, None
    wordcloud_path = None
    if request.method == "POST":
        text = request.form.get("user_input")
        if text:
            result = analyze_sentiment(text)
            if result:
                sentiment = result['sentiment']
                confidence = result['confidence']
                wordcloud_path = generate_wordcloud(text)
    return render_template("index.html", sentiment=sentiment, confidence=confidence, wordcloud=wordcloud_path)

# Batch input analysis route
@app.route("/batch", methods=["POST"])
def batch_analyze():
    file = request.files.get("batch_file")
    if file:
        encoding = detect_encoding(file)
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file, encoding=encoding)
                texts = df.iloc[:, 0].tolist()
            else:
                texts = file.read().decode(encoding).splitlines()

            results = []
            for text in texts:
                result = analyze_sentiment(text)
                if result:
                    results.append({"text": text, "sentiment": result['sentiment'], "confidence": result['confidence']})

            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify({"error": "No file provided."})

# Chatbot route
@app.route('/chat', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    if user_input:
        conversation_history = request.json.get('history', [])
        history_text = "\n".join(f"User: {chat['user']}\nAI: {chat['ai']}" for chat in conversation_history)
        prompt = (
            "You are a conversational assistant. Engage in a friendly and helpful discussion with the user.\n\n"
            f"{history_text}\nUser: {user_input}\nAI:"
        )
        response = sentiment_model.invoke(prompt)
        return jsonify({"response": response})
    return jsonify({"error": "No message provided."})

@app.route('/download_wordcloud')
def download_wordcloud():
    return send_from_directory('static', 'wordcloud.png', as_attachment=True)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
