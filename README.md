# AI_Sentiment_Analyser_using_Flask

AI Sentiment Analyzer is a web-based application built using **Flask** that analyzes the sentiment of a given text input or batch file. It uses AI-powered sentiment analysis to determine whether the sentiment of the input is positive, negative, or neutral. Additionally, it generates a word cloud based on the input text.

## Features
- **Text Sentiment Analysis**: Analyze the sentiment of a single text input.
- **Batch Sentiment Analysis**: Upload a CSV or TXT file containing multiple texts for batch sentiment analysis.
- **Word Cloud Generation**: Generate a word cloud visualizing the most frequent words in the input text.
- **Download Word Cloud**: Option to download the generated word cloud image.
- **Clean and Responsive UI**: Simple and modern interface to interact with the application.

## Technologies Used
- **Flask**: Web framework used to build the application.
- **Python**: Programming language for backend development.
- **Langchain and Ollama**: Sentiment analysis using pre-trained language models.
- **Matplotlib and WordCloud**: Libraries used to generate word clouds.
- **Jinja2**: Templating engine for dynamic HTML rendering.
- **HTML5 and CSS3**: For front-end design and styling.

## Installation

### Prerequisites
1. Python 3.7 or higher
2. `pip` for installing Python dependencies

### Installing Ollama

To use the sentiment analysis model (`OllamaLLM`), you need to install **Ollama**. Follow these instructions based on your platform:

- **For Windows**: Download the latest version of Ollama from the [Ollama website](https://ollama.com/). Install it and make sure it is available in your system's `PATH`.
- **For macOS**: Run the following command in your terminal:
    ```bash
    curl -fsSL https://ollama.com/install.sh | bash
    ```
- **For Linux**: Run the following command in your terminal:
    ```bash
    curl -fsSL https://ollama.com/install.sh | bash
    ```

After installation, make sure the Ollama CLI works by running the following command:
```bash
ollama --version

### Steps to Run Locally

1. Clone this repository to your local machine:https://github.com/Rajeshaligeti/AI_Sentiment_Analyser_using_Flask

   ```bash
   git clone https://github.com/Rajeshaligeti/AI_Sentiment_Analyser_using_Flask.git
   cd AI_Sentiment_Analyser_using_Flask
   
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
