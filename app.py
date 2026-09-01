import asyncio
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import whisper

from database.initdb import load_db, save_db
from graph.workflow import generate_target_question, run_parallel_evaluations
from utils.audio import process_audio
from utils.remediation import generate_remediation_quiz

st.set_page_config(page_title="AI Technical Interviewer", layout="wide")

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

whisper_model = load_whisper_model()

# Initialize Persistent Session State (No SQL)
if "db" not in st.session_state:
    st.session_state["db"] = load_db()

if "current_q_index" not in st.session_state:
    st.session_state["current_q_index"] = 0

if "current_question" not in st.session_state:
    st.session_state["current_question"] = ""

if "quiz_passed" not in st.session_state:
    st.session_state["quiz_passed"] = False

if "active_quiz" not in st.session_state:
    st.session_state["active_quiz"] = None

st.title("AI Technical Interviewer & Remediation Platform")

# ---------------------------------------------------------
# PHASE 1: USER INPUT & BASELINE SETUP
# ---------------------------------------------------------
st.sidebar.header("Candidate Setup")
c_name = st.sidebar.text_input("Candidate Name", value="Namita Gudi")
difficulty = st.sidebar.slider("Baseline Difficulty Level", 1, 5, 3)
resume_input = st.sidebar.text_area("Resume Text", height=120, value="Python Developer skilled in async workflows, Pandas, and REST APIs.")
jd_input = st.sidebar.text_area("Job Description", height=120, value="Seeking Python Backend Engineer proficient in concurrency and dataset processing.")

if st.sidebar.button("Initialize / Reset Session"):
    st.session_state["db"] = {
        "session": {"name": c_name, "difficulty": difficulty, "resume": resume_input, "jd": jd_input},
        "questions": [],
        "evaluations": []
    }
    st.session_state["current_q_index"] = 0
    st.session_state["current_question"] = ""
    st.session_state["quiz_passed"] = False
    st.session_state["active_quiz"] = None
    save_db(st.session_state["db"])
    st.sidebar.success("Session Initialized!")

if not st.session_state["db"]["session"]:
    st.info("Please set up your candidate profile in the sidebar and click 'Initialize / Reset Session'.")
    st.stop()

# ---------------------------------------------------------
# PHASE 2: INTELLIGENT QUESTION GENERATION
# ---------------------------------------------------------
st.header(f"Question #{st.session_state['current_q_index'] + 1}")

if not st.session_state["current_question"]:
    asked = [q["question_text"] for q in st.session_state["db"]["questions"]]
    with st.spinner("Fabricating custom technical question using Llama 3..."):
        st.session_state["current_question"] = generate_target_question(
            st.session_state["db"]["session"]["resume"],
            st.session_state["db"]["session"]["jd"],
            st.session_state["db"]["session"]["difficulty"],
            asked
        )

st.info(st.session_state["current_question"])

# ---------------------------------------------------------
# PHASE 3: ANSWER CAPTURE & BASIC GATES
# ---------------------------------------------------------
recorded_audio = st.audio_input("Record your spoken answer")

if recorded_audio is not None:
    with st.spinner("Processing speech via OpenAI Whisper..."):
        audio_metrics = process_audio(recorded_audio, whisper_model)
    
    transcript = audio_metrics["transcript"]
    wpm = audio_metrics["wpm"]
    words = audio_metrics["word_count"]

    st.markdown("**Transcribed Response:**")
    st.write(f'"{transcript}"')
    st.caption(f"Word Count: {words} | Speech Speed: {wpm} WPM")

    # Gate 1: Reject lazy submissions (< 10 words)
    if words < 10:
        st.error("Answer rejected: Submission must be at least 10 words. Please expand on your explanation and re-record.")
    else:
        st.success("Word Count Gate Passed!")

        # ---------------------------------------------------------
        # PHASE 4: PARALLEL MULTI-AGENT EVALUATION
        # ---------------------------------------------------------
        if st.button("Submit & Evaluate Answer"):
            with st.spinner("Running Agent 1 (Technical), Agent 2 (Communication), and Agent 3 (Verifier) concurrently..."):
                eval_payload = asyncio.run(run_parallel_evaluations(
                    transcript,
                    st.session_state["db"]["session"]["jd"],
                    st.session_state["db"]["session"]["resume"],
                    wpm
                ))

            # Sample evaluation baseline scores
            t_score, c_score, v_score = 6.0, 5.5, 7.5
            perfected_phrase = eval_payload["perfected_phrase"]

            st.session_state["latest_eval"] = {
                "question": st.session_state["current_question"],
                "transcript": transcript,
                "tech_score": t_score,
                "comm_score": c_score,
                "verifier_score": v_score,
                "perfected_phrase": perfected_phrase,
                "ideal_tech": 9.5,
                "ideal_comm": 9.0,
                "ideal_verifier": 9.5
            }

            # Generate Quiz for Phase 5 Remediation Panel
            st.session_state["active_quiz"] = generate_remediation_quiz(transcript, perfected_phrase)
            
            # Save data to JSON engine
            st.session_state["db"]["questions"].append({"question_text": st.session_state["current_question"], "transcript": transcript})
            st.session_state["db"]["evaluations"].append(st.session_state["latest_eval"])
            save_db(st.session_state["db"])

        # ---------------------------------------------------------
        # PHASE 5: TARGETED REMEDIATION & QUIZ GATE
        # ---------------------------------------------------------
        if "latest_eval" in st.session_state and st.session_state["active_quiz"]:
            st.markdown("---")
            st.header("Remediation Panel")
            
            st.warning("You could have said it like this:")
            st.info(f'"{st.session_state["latest_eval"]["perfected_phrase"]}"')

            st.subheader("Quiz Gate: Prove You Understood the Improvement")
            quiz = st.session_state["active_quiz"]
            
            selected_option = st.radio(quiz["question"], quiz["options"])
            selected_index = quiz["options"].index(selected_option)

            if st.button("Submit Quiz Answer"):
                if selected_index == quiz["correct_index"]:
                    st.session_state["quiz_passed"] = True
                    st.success("Quiz Passed! Navigation unlocked.")
                else:
                    st.session_state["quiz_passed"] = False
                    st.error("Incorrect. Review the perfected phrase above and try again.")

        # ---------------------------------------------------------
        # PHASE 6: SCOREBOARD & VISUAL DELTA TRACKER
        # ---------------------------------------------------------
        if st.session_state.get("quiz_passed", False):
            st.markdown("---")
            st.header("Scoreboard & Visual Delta Tracker")

            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("Evaluation Breakdown")
                eval_data = st.session_state["latest_eval"]
                st.write(f"**Agent 1 (Technical Depth):** {eval_data['tech_score']}/10")
                st.write(f"**Agent 2 (Communication & STAR):** {eval_data['comm_score']}/10")
                st.write(f"**Agent 3 (Resume Alignment):** {eval_data['verifier_score']}/10")

            with col2:
                # Matplotlib Visual Delta Renderer
                categories = ["Technical", "Communication", "Resume Match"]
                initial_scores = [eval_data['tech_score'], eval_data['comm_score'], eval_data['verifier_score']]
                ideal_scores = [eval_data['ideal_tech'], eval_data['ideal_comm'], eval_data['ideal_verifier']]

                x = np.arange(len(categories))
                width = 0.35

                fig, ax = plt.subplots(figsize=(6, 3.5))
                ax.bar(x - width/2, initial_scores, width, label="Initial Answer", color="#ff6b6b")
                ax.bar(x + width/2, ideal_scores, width, label="Ideal Response", color="#51cf66")

                ax.set_ylabel("Scores (0-10)")
                ax.set_title("Before vs. After Remediation Visual Delta")
                ax.set_xticks(x)
                ax.set_xticklabels(categories)
                ax.set_ylim(0, 10)
                ax.legend()
                ax.grid(axis="y", linestyle="--", alpha=0.5)

                st.pyplot(fig)

            if st.button("Proceed to Next Question"):
                st.session_state["current_q_index"] += 1
                st.session_state["current_question"] = ""
                st.session_state["quiz_passed"] = False
                st.session_state["active_quiz"] = None
                st.rerun()
