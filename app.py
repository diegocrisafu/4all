from flask import Flask, render_template, request, redirect, url_for, session
from gpt4all import GPT4All

app = Flask(__name__)
app.secret_key = "Bella2001%.."  # Replace with a secure key

# Load the GPT4All model (ensure the model file is in your repo or correct path)
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

# Open a persistent chat session by manually entering the context
chat_session = model.chat_session().__enter__()

# Preload a system prompt to instruct the model to answer like Donald Trump
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
        # Append the user's message to chat history
        session["chat_history"].append({"sender": "User", "message": user_message})
        # Generate a response from the model
        response = chat_session.generate(user_message, max_tokens=256)
        # Append the response to chat history
        session["chat_history"].append({"sender": "Trump", "message": response.strip()})
        session.modified = True
        return redirect(url_for("index"))
    return render_template("index.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(debug=True)
