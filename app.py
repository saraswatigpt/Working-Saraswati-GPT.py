from flask import Flask, render_template, request, session, redirect, url_for
import openai
import os

# Securely get API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = "random-strong-key-1234"

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = []
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        if question.strip():
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",   # GPT-4o model
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": question},
                    ],
                    max_tokens=150,
                    temperature=0.7,
                )
                answer = response.choices[0].message.content.strip()
            except Exception as e:
                answer = f"Error: {str(e)}"
        else:
            answer = "Please enter a question."
        session["history"].append((question, answer))
        session.modified = True
        return redirect(url_for("home"))
    return render_template("index.html", history=session["history"])

@app.route("/reset")
def reset():
    session["history"] = []
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)