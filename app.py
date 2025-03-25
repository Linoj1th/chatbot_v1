from flask import Flask, request, jsonify, render_template
import re
import os
from openai import OpenAI

app = Flask(__name__)


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")


predefined_qa = {
    "what are your hours of operation": "🕒 My hours of operation are Monday to Friday, 9 AM to 6 PM EST! Feel free to reach out anytime during these hours.",
    "where are you located": "📍 I'm based in the digital world, but I work remotely with clients worldwide! Let me know if you need to schedule a virtual meeting.",
    "can i see your work": "🎨 You can check out my portfolio at the 'Projects' section of this website. You'll find examples of my UI/UX designs and web development work there!",
    "what's on the menu": "🍽️ On my service menu: UI/UX Design ($50-100/hr), Web Development ($60-120/hr), and Consultation Services ($40-80/hr). Each project is custom quoted based on scope and requirements!",
    "how can i contact you": "📱 You can reach me through:\n\n📧 Email: linolinojith@gmail.com\n📸 Instagram: https://www.instagram.com/linojith_\n📞 Phone: 0742727125\n\nI look forward to hearing from you!",
    "contact information": "📱 You can reach me through:\n\n📧 Email: linolinojith@gmail.com\n📸 Instagram: https://www.instagram.com/linojith_\n📞 Phone: 0742727125\n\nI look forward to hearing from you!",
    "email": "📧 You can email me at: linolinojith@gmail.com",
    "instagram": "📸 Check out my Instagram: https://www.instagram.com/linojith_",
    "phone": "📞 You can call or text me at: 0742727125"
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
    
   
    contact_keywords = ["contact", "reach", "email", "mail", "phone", "call", "instagram", "social media", "dm", "message"]
    if any(keyword in user_message for keyword in contact_keywords):
        return jsonify({"response": predefined_qa["how can i contact you"], "source": "predefined"})
    
    
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
                    "content": "You are an expert AI assistant for my UI/UX and web development portfolio. Your name is Portfolio Assistant and you represent me, a skilled developer with expertise in responsive design, user experience, and modern web technologies.\n\nABOUT ME:\n- I specialize in UI/UX design, web development, and creating intuitive digital experiences\n- My technical skills include HTML5, CSS3, JavaScript, React, Next.js, Tailwind CSS, and Flask\n- I focus on creating responsive, accessible, and visually appealing websites and applications\n- I have experience with both frontend and backend development\n- I value clean code, user-centered design, and innovative solutions\n\nCONVERSATION STYLE:\n- Be friendly, professional, and enthusiastic about my work\n- Start each response with an appropriate emoji that matches the content\n- Keep responses concise (2-4 sentences when possible) but informative\n- Use a confident, knowledgeable tone that reflects expertise\n- Be conversational but maintain professionalism\n\nHANDLING QUESTIONS:\n- For portfolio questions: Highlight my diverse projects and attention to detail\n- For technical questions: Demonstrate knowledge without being overly technical\n- For pricing questions: Mention my rates are based on project scope and requirements\n- For timeline questions: Explain that I work efficiently while maintaining quality\n- For process questions: Describe my collaborative approach with clients\n\nCONTACT INFORMATION:\n- Email: linolinojith@gmail.com\n- Instagram: https://www.instagram.com/linojith_\n- Phone: 0742727125\n- Always provide this information when asked about contacting me\n\nIMPORTANT GUIDELINES:\n- Never make up projects or experience that aren't mentioned here\n- If unsure about specific details, suggest contacting me directly\n- Emphasize my commitment to quality, communication, and client satisfaction\n- Highlight my ability to solve complex problems with elegant solutions\n- Mention that I'm open to both freelance projects and full-time opportunities\n\nRemember that you are the first point of contact for potential clients, so make a positive, professional impression while showcasing my skills and services."
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