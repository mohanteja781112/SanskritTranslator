
from dotenv import load_dotenv
load_dotenv()
# OPEN_KEY='rmOgvR28J-m-tX5bfBQVUej_nAENfkEo-Vbi0qu6JqE'

from flask import Flask, render_template_string, request
from boltiotai import openai
import os
import sys

# Use API key from environment variable (Replit Secrets Tool recommended)
openai.api_key = 'rmOgvR28J-m-tX5bfBQVUej_nAENfkEo-Vbi0qu6JqE'

if not openai.api_key:
    sys.stderr.write("""
    ❌ You haven't set up your API key yet.

    To fix:
    1. Go to Replit Secrets (🔒 icon in left sidebar)
    2. Add key: OPENAI_API_KEY = your-boltiotai-key
    """)
    exit(1)

app = Flask(__name__)

# HTML + CSS template
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sanskrit Translator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f8ff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .translator-box {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            width: 500px;
        }
        textarea, select, button {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        h2 {
            text-align: center;
        }
        .output {
            margin-top: 15px;
            background: #f9f9f9;
            padding: 10px;
            border-left: 4px solid #4CAF50;
        }
    </style>
</head>
<body>
    <div class="translator-box">
        <h2>Sanskrit Translator</h2>
        <form method="POST">
            <label for="sanskrit">Enter Sanskrit Text:</label>
            <textarea name="sanskrit" required>{{ sanskrit or '' }}</textarea>

            <label for="lang">Translate to:</label>
            <select name="lang">
                <option value="te" {% if lang == 'te' %}selected{% endif %}>Telugu</option>
                <option value="en" {% if lang == 'en' %}selected{% endif %}>English</option>
            </select>

            <button type="submit">Translate</button>
        </form>
        {% if translated %}
        <div class="output">
            <strong>Translated Text ({{ 'Telugu' if lang == 'te' else 'English' }}):</strong>
            <p>{{ translated }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    sanskrit_text = ""
    lang = "en"

    if request.method == 'POST':
        sanskrit_text = request.form['sanskrit']
        lang = request.form['lang']

        if lang == "te":
            prompt = (
                # f"ఈ సంస్కృత శ్లోకం యొక్క భావాన్ని తెలుగులో సులభంగా అర్థమయ్యేలా వివరించండి. "
                # f"తెలుగు పదాలు మాత్రమే వాడండి. ఇంగ్లీష్ పదాలు, ట్రాన్స్‌లిటరేషన్ (లిప్యంతరణ) వాడకండి. "
                # f"శ్లోకం యొక్క పూర్ణార్థం తెలుగులో చెప్పండి:\n\n\"{sanskrit_text}\""
                f"Translate the following sanskrit sentence to Telugu with no English words:\n\n\"{sanskrit_text}"
            )
        else:
            prompt = (
                f"Translate the following sanskrit sentence to English and if we click translate button n number of times it should give a constant(same) meaning:\n\n\"{sanskrit_text}\""
            )





        try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that accurately translates Sanskrit into Telugu or English."},
                        {"role": "user", "content": prompt}
                    ]
                )
                translated_text = response['choices'][0]['message']['content'].strip()

        except Exception as e:
                translated_text = f"Error: {e}"


    return render_template_string(template, translated=translated_text, sanskrit=sanskrit_text, lang=lang)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

