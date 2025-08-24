# AI Sentiment Analyzer using Flask 

AI Sentiment Analyzer is a web-based application built using **Flask** that analyzes the sentiment of text input or batch files. It uses Google's **Gemini AI** for advanced sentiment analysis to determine whether the sentiment is positive, negative, neutral, or mixed. The application also generates word clouds and includes a conversational chatbot feature.

### Website link : ![WEBSITE🤖](https://ai-sentiment-analyser-using-flask.onrender.com/)
### Application Interface
Here's a screenshot of the application's interface:

![Application UI](media/ui_screenshot.png)

### Word Cloud Example
Below is an example of the generated word cloud:

![Word Cloud](media/wordcloud_example.png)

### Sentiment Result
Here is a screenshot of the application's output:

![Output](media/Sentiment_analysis.png)

## Features
- **Text Sentiment Analysis**: Analyze the sentiment of single text input with confidence scores
- **Batch Sentiment Analysis**: Upload CSV, TXT, or Excel files for batch processing (up to 100 entries)
- **Multiple File Formats**: Support for .csv, .txt, .xlsx, and .xls files
- **Word Cloud Generation**: Visualize the most frequent words in your text
- **Download Word Cloud**: Save generated word clouds as PNG files
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Processing**: Instant results with progress indicators
- **Clean and Responsive UI**: Simple and modern interface to interact with the application.

## Technologies Used
- **Flask**: Web framework for the application backend
- **Google Gemini AI**: Advanced language model for sentiment analysis
- **Langchain**: Framework for LLM integration and prompt management
- **Python**: Core programming language
- **Pandas**: Data processing for batch analysis
- **Matplotlib & WordCloud**: Visualization libraries
- **Jinja2**: Templating engine for dynamic HTML rendering.
- **HTML5 and CSS3**: For front-end design and styling.
- **JavaScript**: Interactive frontend functionality

## Installation

### Prerequisites
1. Python 3.11 or higher
2. Google Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
3. `pip` for installing Python dependencies

### Quick Setup
1. Clone this repository to your local machine:https://github.com/Rajeshaligeti/AI_Sentiment_Analyser_using_Flask
   ```bash
   git clone https://github.com/Rajeshaligeti/AI_Sentiment_Analyser_using_Flask.git
   cd AI_Sentiment_Analyser_using_Flask
   ```

2. Create a virtual environment (recommended):
    On Windows:
    bash
    python -m venv venv
    venv\Scripts\activate

    On macOS/Linux:
    bash
    python3 -m venv venv
    source venv/bin/activate

3. Install the dependencies:
    bash
    pip install -r requirements.txt

4. Run the Flask application:
    bash
    python app.py

5. Open your web browser and visit http://127.0.0.1:5000/ to use the application. 



### License
This project is licensed under the [Apache License 2.0](LICENSE).  
Feel free to use, modify, and distribute the code as per the terms of the license.

