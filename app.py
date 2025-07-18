from flask import Flask, render_template, request, redirect, url_for, session, send_file
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = "supersecret"  # Change this in production

# Keys (ENV variables, safe)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "YOUR_OPENWEATHER_KEY")
IMAGE_API_KEY = os.environ.get("IMAGE_API_KEY", "YOUR_IMAGE_GEN_KEY")  # Optional

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # "gemini-pro" bhi likh sakte ho

# Weather util
def get_weather(query):
    # Very basic location extractor (improve with NLP if needed)
    import re
    match = re.search(r"(?:weather in |weather at |weather |temperature in |temperature at )?([A-Za-z ]+)", query.lower())
    city = match.group(1).strip() if match else None
    if not city:
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        res = requests.get(url, timeout=8)
        data = res.json()
        if data.get("cod") != 200:
            return f"Sorry, weather info for '{city.title()}' not found."
        weather = data['weather'][0]['main']
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"🌦️ Weather in {city.title()}: {weather}, {desc}, {temp}°C"
    except Exception as e:
        return f"Weather API error: {e}"

# Dummy image gen (replace with actual API if needed)
def generate_image(prompt):
    # For real use: Connect DALL·E, Replicate, HuggingFace, etc.
    return "https://placehold.co/400x250?text=Image+Not+Implemented"  # Placeholder

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = []
    history = session["history"]

    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            # --- Weather Command ---
            if any(word in question.lower() for word in ["weather", "temperature"]):
                answer = get_weather(question)
            # --- Image Generation ---
            elif question.lower().startswith("/imagine ") or question.lower().startswith("draw "):
                prompt = question.split(" ", 1)[1]
                img_url = generate_image(prompt)
                answer = f'<img src="{img_url}" alt="Generated Image" style="max-width:96%;border-radius:11px;" />'
            # --- Gemini Chat AI ---
            else:
                try:
                    response = model.generate_content(question)
                    answer = response.text
                except Exception as e:
                    answer = f"Error: {e}"
            history.append((question, answer))
            session["history"] = history
    return render_template("index.html", history=history)

@app.route("/reset")
def reset():
    session["history"] = []
    return redirect(url_for("home"))

# Download history as txt
@app.route("/download")
def download():
    history = session.get("history", [])
    content = "\n\n".join([f"You: {q}\nSaraswatiGPT: {a}" for q, a in history])
    with open("history.txt", "w", encoding="utf-8") as f:
        f.write(content)
    return send_file("history.txt", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)