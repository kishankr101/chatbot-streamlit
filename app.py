from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="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")

app = Flask(__name__)

# HTML + JS (frontend in same file)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chatbot</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; }
        #chatbox { width: 400px; margin: 50px auto; background: white; padding: 20px; border-radius: 10px; }
        #messages { height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
        input { width: 75%; padding: 10px; }
        button { padding: 10px; }
        .user { color: blue; }
        .bot { color: green; }
    </style>
</head>
<body>

<div id="chatbox">
    <h2>Chatbot</h2>
    <div id="messages"></div>
    <input id="input" placeholder="Type a message..." />
    <button onclick="sendMessage()">Send</button>
</div>

<script>
async function sendMessage() {
    let input = document.getElementById("input");
    let message = input.value;
    if (!message) return;

    let messagesDiv = document.getElementById("messages");

    messagesDiv.innerHTML += "<div class='user'><b>You:</b> " + message + "</div>";

    input.value = "";

    let response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    });

    let data = await response.json();

    messagesDiv.innerHTML += "<div class='bot'><b>Bot:</b> " + data.reply + "</div>";
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": user_message}]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
