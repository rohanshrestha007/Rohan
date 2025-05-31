from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # Allow requests from your frontend

openai.api_key = "YOUR_OPENAI_API_KEY"  # <-- keep this secret, never in frontend

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '').lower()
    # Simple AI logic
    if 'author' in question or 'developer' in question or 'who made' in question:
        answer = "👨‍💻 This website was created by Rohan Shrestha (Vaidya) using his brain and a little help from AI!"
    elif 'email' in question:
        answer = "📧 You can email me at rohanxtha970@gmail.com"
    elif 'where are you from' in question or 'hometown' in question:
        answer = "🏡 I'm from Dharan, Nepal!"
    else:
        answer = "🤖 Sorry, I can only answer basic questions about the author or this website!"
    return jsonify({'answer': answer})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '').strip()
    q_lower = question.lower()
    # Custom answers
    if any(x in q_lower for x in ['author', 'developer', 'dev', 'who made', 'who created']):
        answer = "👨‍💻 This website was created by Rohan Shrestha (Vaidya) and help from AI!"
    elif 'email' in q_lower:
        answer = "📧 You can email me at rohanxtha970@gmail.com"
    elif 'where are you from' in q_lower or 'hometown' in q_lower:
        answer = "🏡 I'm from Dharan, Nepal!"
    elif q_lower in ['hello', 'hi', 'hey']:
        answer = "👋 Hello! How can I help you?"
    elif q_lower == 'wtf':
        answer = "😅 Let's keep it friendly! How can I help you?"
    else:
        # Use OpenAI GPT for all other questions
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
                messages=[{"role": "user", "content": question}],
                max_tokens=200,
                temperature=0.7,
            )
            answer = response.choices[0].message.content.strip()
        except Exception:
            answer = "🤖 Sorry, I couldn't get an answer from OpenAI."
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

# Frontend code snippet for making a request to the /ask endpoint
# const res = await fetch('https://your-backend-url/ask', {
#   method: 'POST',
#   headers: { 'Content-Type': 'application/json' },
#   body: JSON.stringify({ question: q })
# });