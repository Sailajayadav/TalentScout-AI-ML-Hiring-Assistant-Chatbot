#!/usr/bin/env python3
"""
TalentScout Backend Server
Flask API for candidate screening with Gemini AI
"""
import os
import json
import re
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the Gemini client
from gemini_client import GeminiClient
from prompts import NORMALIZE_STACK_TEMPLATE, QUESTION_GENERATION_TEMPLATE

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize Gemini client
gemini = GeminiClient()

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')

@app.route('/api/generate-questions', methods=['POST'])
def generate_questions_endpoint():
    """
    API endpoint to generate interview questions based on candidate tech stack.
    
    Request JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "techStack": "Python, FastAPI, PostgreSQL",
        ...
    }
    
    Response JSON:
    {
        "questions": [
            {
                "name": "Python",
                "questions": [
                    {"q": "Question text", "difficulty": "medium"},
                    ...
                ]
            },
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        tech_stack_raw = data.get('techStack', '')

        if not tech_stack_raw:
            return jsonify({'error': 'Tech stack is required'}), 400

        # Step 1: Normalize tech stack
        print(f"Normalizing tech stack: {tech_stack_raw[:100]}...")
        prompt_normalize = NORMALIZE_STACK_TEMPLATE.format(raw_text=tech_stack_raw)
        normalized = gemini.generate(prompt_normalize, max_tokens=100, temperature=0.0)
        print(f"Normalized: {normalized}")
        
        tech_list = [t.strip() for t in normalized.split(',') if t.strip()]
        if not tech_list:
            tech_list = ['General Knowledge']

        # Step 2: Generate questions for each tech
        print(f"Generating questions for: {tech_list}")
        prompt_generate = QUESTION_GENERATION_TEMPLATE.format(tech_list=', '.join(tech_list))
        raw_response = gemini.generate(prompt_generate, max_tokens=1000, temperature=0.2)
        print(f"Raw response length: {len(raw_response)}")

        # Step 3: Parse JSON response
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
            else:
                # If no JSON found, create a default structure
                parsed = {
                    "tech": [
                        {
                            "name": t,
                            "questions": [
                                {"q": f"Question about {t}", "difficulty": "medium"}
                                for _ in range(3)
                            ]
                        }
                        for t in tech_list
                    ]
                }
        except json.JSONDecodeError as je:
            print(f"JSON parse error: {je}")
            # Fallback: create default questions
            parsed = {
                "tech": [
                    {
                        "name": t,
                        "questions": [
                            {"q": f"Explain a key concept in {t}", "difficulty": "medium"},
                            {"q": f"Describe a real-world application of {t}", "difficulty": "medium"},
                            {"q": f"What are the best practices for {t}?", "difficulty": "hard"}
                        ]
                    }
                    for t in tech_list
                ]
            }

        # Return the questions
        return jsonify({
            'questions': parsed.get('tech', [])
        }), 200

    except Exception as e:
        print(f"Error in generate_questions: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'gemini_available': not gemini._mock}), 200

if __name__ == '__main__':
    print("Starting TalentScout Backend Server...")
    try:
        is_mock = hasattr(gemini, '_mock') and gemini._mock
        print(f"Gemini client mock mode: {is_mock}")
    except Exception:
        print("Gemini client initialized")
    print(f"Model: {gemini.model}")
    print("Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
