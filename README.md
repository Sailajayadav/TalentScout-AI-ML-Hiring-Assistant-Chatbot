📘 TalentScout – AI-Powered Technical Screening Assistant

An intelligent recruitment chatbot built using Flask (Python), Gemini 2.0 Flash LLM, and a modern HTML/CSS/JavaScript frontend.
TalentScout automates the candidate screening process by collecting essential details, understanding tech stacks, and generating customized technical interview questions.

🚀 Project Overview

TalentScout is a full-stack, AI-driven screening assistant designed for recruitment workflows.
It performs:

Candidate information collection

Tech-stack extraction & normalization

Dynamic interview question generation using Gemini 2.0 Flash

Structured interview workflow with progress tracking

Modern UI using TailwindCSS

REST APIs with Flask

Contextual and structured prompt engineering

This project fulfills an AI/ML assignment requiring prompt engineering, LLM use, UI design, and backend integration.

🧠 Key Capabilities
✔ 1. Candidate Information Collection

The chatbot gathers:

Full Name

Email

Phone

Years of Experience

Desired Position

Current Location

Tech Stack

✔ 2. Smart Tech Stack Normalization

Tech stack text (free-form, messy) is cleaned using an LLM prompt into normalized technologies.

✔ 3. Dynamic Question Generation

For each technology, the system generates exactly 3 questions, each with:

Question text

Difficulty level (easy/medium/hard)

✔ 4. Friendly and Modern UI

The frontend is built with:

HTML

TailwindCSS

Vanilla JavaScript

Animated transitions

✔ 5. REST API with Flask

Backend endpoints:

Endpoint	Method	Purpose
/	GET	Loads UI
/api/generate-questions	POST	Generates questions from tech stack
/api/health	GET	Health check
✔ 6. Fully LLM-Driven Prompt Engineering

Prompts control:

Greeting

Information gathering

Tech normalization

Question generation

🏗️ Project Structure
pgagi/
│── server.py                # Flask backend
│── gemini_client.py         # Gemini API wrapper
│── prompts.py               # Prompt templates
│── storage.py               # Simulated candidate storage
│── templates/
│     └── index.html         # Full frontend
│── static/
│     └── (Tailwind loaded via CDN)
│── requirements.txt
│── Procfile                 # Render deployment
│── .env (local only)
│── README.md

⚙️ Technical Details
🔧 Backend (Flask)

Flask + CORS

Google Generative AI SDK (google-generativeai)

Custom Gemini client wrapper

JSON parsing with fallback

Simulated storage using storage.py

🎨 Frontend

TailwindCSS (CDN)

Modern, animated UI (fade-in, slide-up)

JavaScript state management

Dynamic rendering (info → generating → interview stages)

🧠 Gemini Model

Model used:

models/gemini-2.0-flash

📦 Dependencies (requirements.txt)

Must include:

Flask
flask-cors
python-dotenv
google-generativeai
gunicorn

🎯 Prompt Design
1. Normalization Prompt

Used to convert messy tech stack input into clean comma-separated tags:

Turn the following into a clean, comma-separated list of technologies.
Input: "{raw_text}"
Output format: tech1, tech2, tech3

2. Question Generation Prompt

For each technology:

Generate exactly 3 questions

Each containing question text + difficulty

Returned strictly as JSON.

3. System Prompt

Controls tone and behavior (in GREET_PROMPT).

🧪 How to Run Locally
1️⃣ Clone Repository
git clone <your-repository-url>
cd pgagi

2️⃣ Set up environment

Create .env:

GEMINI_API_KEY=your_api_key_here

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run Flask server
python server.py

5️⃣ Visit in browser
http://localhost:5000

🌐 Deployment Guide (Render.com)
1. Add Procfile
web: gunicorn server:app

2. Deploy Steps

Push project to GitHub

Go to Render → New Web Service

Select repository

Set:

Setting	Value
Build Command	pip install -r requirements.txt
Start Command	gunicorn server:app
Instance	Free
Region	Singapore

Add environment variable:

GEMINI_API_KEY = your-api-key


Click Deploy

✔ If successful, you will receive a public URL
✔ If there are errors, check logs or share them for assistance

📚 Challenges & Solutions
Challenge	Solution
LLM returning messy text	Added regex-based JSON extraction + fallback
Tech stack inconsistencies	Added normalization prompt
Gemini 2.0 API changes	Replaced old genai.Client() with GenerativeModel
JSON parsing failures	Implemented default questions when parsing breaks
Deployment errors on Render	Fixed import (import google.generativeai as genai) & updated Procfile
🧩 Architectural Highlights

MVC-like separation

UI in HTML

Logic in JS

Backend routes in Flask

GeminiClient class

Clean wrapper for API calls

Handles exceptions + token config

Prompt modularity

Easier debugging

Reusable templates

Robust JSON processing

Handles LLM imperfections gracefully

🏁 Conclusion

TalentScout is a fully working, production-ready screening assistant demonstrating:

Prompt engineering mastery

Full-stack development

LLM integration

API design

UI development

Deployment skills

It satisfies all assignment requirements for:
✔ Prompt design
✔ Data handling
✔ Documentation
✔ Functional UI
✔ LLM-powered workflows
✔ Version control

