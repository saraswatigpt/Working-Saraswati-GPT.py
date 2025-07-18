from flask import Flask, render_template, request, session, redirect, url_for
import openai

openai.api_key = "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"

app = Flask(__name__)
app.secret_key = "saraswatiGPT-secret-key"

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = []
    answer = ""
    image_url = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        image_prompt = request.form.get("image_prompt", "")
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
        if image_prompt.strip():
            try:
                image = openai.Image.create(
                    prompt=image_prompt,
                    n=1,
                    size="512x512"
                )
                image_url = image["data"][0]["url"]
            except Exception as e:
                image_url = ""
        session["history"] += [[question, answer, image_prompt, image_url]]
        session.modified = True
        return redirect(url_for("home"))
    return render_template("index.html", history=session["history"])

@app.route("/reset")
def reset():
    session["history"] = []
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)