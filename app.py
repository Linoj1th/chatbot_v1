from flask import Flask, request, jsonify, render_template
import re
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

app = Flask(__name__)


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")


predefined_qa = {
     "how to contact you": "🕒linolinojith@gmail.com  this is my gmail you can sent mail to me",
    "what are your hours of operation": "🕒 My hours of operation are Monday to Friday, 9 AM to 6 PM EST! Feel free to reach out anytime during these hours.",
    "where are you located": "📍 I'm based in the digital world, but I work remotely with clients worldwide! Let me know if you need to schedule a virtual meeting.",
    "can i see your work": "🎨 You can check out my portfolio at the 'Projects' section of this website. You'll find examples of my UI/UX designs and web development work there!",
    "what's on the menu": "🍽️ On my service menu: UI/UX Design ($50-100/hr), Web Development ($60-120/hr), and Consultation Services ($40-80/hr). Each project is custom quoted based on scope and requirements!"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower().strip()
    
   
    for question, answer in predefined_qa.items():
        if re.search(r'\b' + re.escape(question) + r'\b', user_message):
            return jsonify({"response": answer, "source": "predefined"})
    
 
    try:
      
        if not OPENROUTER_API_KEY:
            return jsonify({
                "response": "😓 API key not configured. Please set the OPENROUTER_API_KEY environment variable.",
                "source": "error"
            })
            
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": request.host_url,
                "X-Title": "Portfolio AI Assistant",
            },
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly and helpful assistant for my personal UI/UX and web development portfolio. You represent me and should answer questions about my work, skills, and services. Keep responses concise, professional, and add an appropriate emoji at the beginning."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        
        ai_response = completion.choices[0].message.content
        return jsonify({"response": ai_response, "source": "ai"})
    
    except Exception as e:
        return jsonify({"response": f"😓 Sorry, I encountered an error: {str(e)}", "source": "error"})

if __name__ == '__main__':
    app.run(debug=True)