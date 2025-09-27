from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key in environment variable before running
openai.api_key = os.getenv("OPENAI_API_KEY")

# System prompt for GardenMate
SYSTEM_PROMPT = (
    "You are GardenMate — a helpful, concise, practical home gardening assistant. "
    "You give advice about plant care, watering schedules, soil, sunlight, "
    "and safe non-chemical pest solutions. "
    "If users provide plant names or describe symptoms, suggest diagnostics and remedies."
)

# Store conversation in memory (per session)
conversation = [{"role": "system", "content": SYSTEM_PROMPT}]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please type something!"})

    conversation.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=conversation,
            max_tokens=500,
            temperature=0.7,
        )
        bot_reply = response.choices[0].message["content"].strip()
        conversation.append({"role": "assistant", "content": bot_reply})
        return jsonify({"response": bot_reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
