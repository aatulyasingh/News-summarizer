from flask import Flask, render_template, jsonify
from groq import Groq
from dotenv import load_dotenv
import requests
import os

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
client = Groq(api_key=GROQ_API_KEY)

def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    headlines = []
    for article in articles:
        headlines.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"]
        })
    return headlines

def summarize_news(headlines):
    headline_text = "\n".join([f"- {h['title']}" for h in headlines])
    prompt = f"""Here are today's top news headlines:

{headline_text}

Please give me a brief, friendly summary of what's happening in the world today."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-news")
def get_news():
    headlines = fetch_news()
    summary = summarize_news(headlines)
    return jsonify({
        "headlines": headlines,
        "summary": summary
    })

if __name__ == "__main__":
    app.run(debug=True)