from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "supersecret"  # Session ke liye zaruri

# Gemini API KEY env se lo ya seedha yahan likho (demo ke liye)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YAHAN_APNI_API_KEY_DAL")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # "gemini-pro" bhi likh sakte ho

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = []
    history = session["history"]

    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
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

if __name__ == "__main__":
    app.run(debug=True)