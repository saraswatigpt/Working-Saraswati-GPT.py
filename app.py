from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

# Gemini API KEY ko env variable se le, ya direct yahan likh de (for demo only)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YAHAN_APNI_API_KEY_DAL")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Ya gemini-pro, as per your key

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            try:
                response = model.generate_content(question)
                answer = response.text
            except Exception as e:
                answer = f"Error: {e}"
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)