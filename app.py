from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chat memory (session-wide)
conversation = [
    {"role": "system", "content": "You are a professional AI assistant."}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation

    message = request.form.get("message", "")
    file = request.files.get("file")

    if file:
        filename = file.filename.lower()

        # Image upload
        if filename.endswith((".png", ".jpg", ".jpeg")):
            user_content = f"The user uploaded an image named {filename}. Acknowledge it politely."
        else:
            # Text / code file
            content = file.read().decode("utf-8", errors="ignore")
            user_content = f"Here is the uploaded file content:\n{content}"

    else:
        user_content = message

    conversation.append({"role": "user", "content": user_content})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

@app.route("/new-chat", methods=["POST"])
def new_chat():
    global conversation
    conversation = [
        {"role": "system", "content": "You are a professional AI assistant."}
    ]
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
