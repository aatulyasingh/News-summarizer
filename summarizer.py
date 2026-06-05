from groq import Groq
from dotenv import load_dotenv
import requests
import os

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    headlines = []
    for article in articles:
        headlines.append(f"- {article['title']}")
    return "\n".join(headlines)

def summarize_news(headlines):
    prompt = f"""Here are today's top news headlines:

{headlines}

Please give me a brief, friendly summary of what's happening in the world today."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    print("📰 Fetching today's top news...\n")
    headlines = fetch_news()
    print("Headlines found:\n")
    print(headlines)
    print("\n🤖 Generating AI summary...\n")
    summary = summarize_news(headlines)
    print("TODAY'S NEWS SUMMARY:")
    print("=" * 40)
    print(summary)

if __name__ == "__main__":
    main()