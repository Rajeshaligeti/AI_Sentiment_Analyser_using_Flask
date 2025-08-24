from flask import Flask, render_template, request, jsonify
from flask import send_from_directory
import google.generativeai as genai
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import re
import chardet
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load sentiment model
def load_sentiment_model():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-1.5-flash')  

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
    
    prompt = (
        "You are an AI sentiment analyzer that interprets all types of inputs, including informal, rude, or slang language. "
        "Please return the sentiment (positive, negative, neutral, or mixed) and a confidence score (0 to 1), regardless of the input.\n"
        f"Input: {preprocessed_text}\n"
        "Response format: Sentiment: [sentiment] Confidence: [score]"
    )
    
    try:
        response = sentiment_model.generate_content(prompt)
        return parse_sentiment_response(response.text)
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return {"sentiment": "Neutral", "confidence": 0.5}

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
    if 'batch_file' not in request.files:
        return jsonify({"error": "No file part in the request."})
    
    file = request.files['batch_file']
    
    if file.filename == '' or file.filename is None:
        return jsonify({"error": "No file selected."})
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Please upload .txt, .csv, .xlsx, or .xls files."})
    
    try:
        # Save the file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the file
        texts = []
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
            texts = df.iloc[:, 0].astype(str).tolist()
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
            texts = df.iloc[:, 0].astype(str).tolist()
        else:  # .txt file
            with open(filepath, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f.readlines() if line.strip()]

        # Clean up the temporary file
        os.remove(filepath)

        # Analyze sentiments
        results = []
        for i, text in enumerate(texts[:100]):  # Limit to 100 entries for performance
            if text and len(text.strip()) > 0:
                result = analyze_sentiment(text)
                if result:
                    results.append({
                        "id": i + 1,
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "sentiment": result['sentiment'], 
                        "confidence": result['confidence']
                    })

        return jsonify({
            "success": True,
            "total_processed": len(results),
            "results": results
        })
        
    except Exception as e:
        # Clean up the file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": f"Error processing file: {str(e)}"})
    
    return jsonify({"error": "Unknown error occurred."})

# Chatbot route
@app.route('/chat', methods=['POST'])
def chatbot():
    if not request.json:
        return jsonify({"error": "No JSON data provided."})
    
    user_input = request.json.get('message')
    if user_input:
        conversation_history = request.json.get('history', [])
        history_text = "\n".join(f"User: {chat['user']}\nAI: {chat['ai']}" for chat in conversation_history)
        
        prompt = (
            "You are a conversational assistant. Engage in a friendly and helpful discussion with the user.\n\n"
            f"{history_text}\nUser: {user_input}\nAI:"
        )
        
        try:
            response = sentiment_model.generate_content(prompt)
            return jsonify({"response": response.text})
        except Exception as e:
            print(f"Error in chatbot: {e}")
            return jsonify({"error": "Sorry, I'm having trouble responding right now."})
    return jsonify({"error": "No message provided."})

@app.route('/download_wordcloud')
def download_wordcloud():
    return send_from_directory('static', 'wordcloud.png', as_attachment=True)

# Run the app
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
