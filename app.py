import os
from flask import Flask, render_template, request, redirect, url_for, session
from gpt4all import GPT4All

app = Flask(__name__)
# Flask uses the secret key for session security; you can generate one with Python's secrets module.
app.secret_key = "Bella2001%.."  # Replace with a secure, random key for production

# Load the GPT4All model (ensure the model file is accessible; adjust the model name/path as needed)
model = GPT4All("DeepSeek-R1-Distill-Qwen-7B")  # You might need to include file extension if required

# Open a persistent chat session by manually entering the context manager
chat_session = model.chat_session().__enter__()

# Preload a system prompt instructing the model to answer like Donald Trump
system_prompt = (
    "You are Donald Trump. Answer all questions in a manner consistent with Donald Trump's speaking style, "
    "using his signature phrases and tone. For example, use phrases like 'Make America Great Again!' and "
    "'Nobody builds walls better than me.'"
)
chat_session.generate(system_prompt, max_tokens=150)

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []
    if request.method == "POST":
        user_message = request.form["message"]
        # Save the user's message
        session["chat_history"].append({"sender": "User", "message": user_message})
        # Generate a response from the model
        response = chat_session.generate(user_message, max_tokens=256)
        # Save the model's response
        session["chat_history"].append({"sender": "Trump", "message": response.strip()})
        session.modified = True
        return redirect(url_for("index"))
    return render_template("index.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    # Listen on the port specified by the environment variable, defaulting to 5000 locally.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
