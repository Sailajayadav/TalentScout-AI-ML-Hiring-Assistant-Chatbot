# app.py
import streamlit as st
import os
import json
import re
from dotenv import load_dotenv
load_dotenv()

from gemini_client import GeminiClient
from prompts import NORMALIZE_STACK_TEMPLATE, QUESTION_GENERATION_TEMPLATE
from storage import save_candidate

EXIT_KEYWORDS = os.getenv("EXIT_KEYWORDS", "quit,exit,bye,stop,goodbye").split(",")

# --------------- UI ----------------
st.set_page_config(page_title="TalentScout — Gemini 2.0 Flash", layout="centered")
st.title("TalentScout — Tech Screening Assistant")
st.caption("Powered by Gemini 2.0 Flash ⚡ Fast, Stable & Free")

# --------------- Gemini Client ----------------
client = GeminiClient(model="models/gemini-2.0-flash")


# --------------- SESSION STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "collect_info"
if "questions" not in st.session_state:
    st.session_state.questions = []
if "tech_index" not in st.session_state:
    st.session_state.tech_index = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {}


# -------------------- STAGE 1 --------------------
if st.session_state.stage == "collect_info":
    st.subheader("Candidate Information")

    with st.form("candidate_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        exp = st.number_input("Years of Experience", min_value=0, max_value=60)
        pos = st.text_input("Desired Position(s)")
        loc = st.text_input("Current Location")
        tech_raw = st.text_area("Describe your tech stack")
        start = st.form_submit_button("Start Screening")

    if start:
        if not name or not email or not tech_raw:
            st.warning("Full Name, Email, and Tech Stack are required.")
        else:
            st.session_state.candidate = {
                "full_name": name,
                "email": email,
                "phone": phone,
                "years_experience": exp,
                "desired_positions": pos,
                "location": loc
            }

            # Normalize tech stack using Gemini
            prompt = NORMALIZE_STACK_TEMPLATE.format(raw_text=tech_raw)
            normalized = client.generate(prompt, max_tokens=80, temperature=0.0)

            tech_list = [t.strip() for t in normalized.split(",") if t.strip()]

            st.write("Detected Tech Stack:", tech_list)
            st.session_state.candidate["tech_stack"] = tech_list

            st.session_state.stage = "generate_questions"
            st.rerun()


# -------------------- STAGE 2 --------------------
if st.session_state.stage == "generate_questions":
    st.subheader("Generating Technical Questions...")

    tech_list = st.session_state.candidate["tech_stack"]
    prompt = QUESTION_GENERATION_TEMPLATE.format(
        tech_list=", ".join(tech_list)
    )

    raw = client.generate(prompt, max_tokens=600, temperature=0.3)

    try:
        block = re.search(r"\{.*\}", raw, re.DOTALL)
        parsed = json.loads(block.group(0))
    except:
        st.error("Model returned invalid JSON:")
        st.code(raw)
        st.stop()

    st.session_state.questions = parsed["tech"]
    st.session_state.chat_history.append({
        "role": "assistant",
        "msg": "Great! Let's begin your interview!"
    })

    st.session_state.stage = "interview"
    st.rerun()


# -------------------- STAGE 3 --------------------
if st.session_state.stage == "interview":
    st.subheader("Technical Interview")

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["msg"])

    tech_blocks = st.session_state.questions
    t = st.session_state.tech_index
    q = st.session_state.q_index

    # End of interview
    if t >= len(tech_blocks):
        st.success("Interview complete!")
        anon = save_candidate({
            **st.session_state.candidate,
            "generated_questions": st.session_state.questions
        })
        st.write("Your Anonymized ID:", anon)
        st.stop()

    tech = tech_blocks[t]
    tech_name = tech["name"]
    current_q = tech["questions"][q]["q"]

    st.chat_message("assistant").write(f"({tech_name}) — {current_q}")

    ans = st.chat_input("Your answer:")
    if ans:
        st.session_state.chat_history.append({"role": "user", "msg": ans})

        if q + 1 < len(tech["questions"]):
            st.session_state.q_index += 1
        else:
            st.session_state.tech_index += 1
            st.session_state.q_index = 0
            st.session_state.chat_history.append({
                "role": "assistant",
                "msg": "Moving to next topic..."
            })

        st.rerun()
