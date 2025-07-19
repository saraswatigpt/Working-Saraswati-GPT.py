from flask import Flask, render_template, request, session, redirect, url_for
import os
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "supersecret"  # Change in production

# Gemini API Key (store as env var in Render/Cloud)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = []
    history = session["history"]
    if request.method == "POST":
        question = request.form.get("question", "")
        answer = ""
        if question:
            try:
                response = model.generate_content(question)
                answer = response.text
            except Exception as e:
                answer = f"Error: {e}"
            history.append((question, answer))
            session["history"] = history
            session.modified = True
        return redirect(url_for("home"))
    return render_template("index.html", history=history)

@app.route("/reset")
def reset():
    session["history"] = []
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)