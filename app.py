from flask import Flask, render_template, request, session, redirect, url_for
import openai

openai.api_key = "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"

app = Flask(__name__)
app.secret_key = "kuchbhi_random_secret_key_9876"

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = []
    answer = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        if question.strip():
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": question}],
                    max_tokens=150,
                    temperature=0.7,
                )
                answer = response.choices[0].message.content.strip()
            except Exception as e:
                answer = "Error: " + str(e)
        else:
            answer = "Please enter a question."
        # Add to history
        session["history"].append((question, answer))
        session.modified = True
        return redirect(url_for("home"))
    return render_template("index.html", history=session["history"])

@app.route("/reset")
def reset():
    session["history"] = []
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()