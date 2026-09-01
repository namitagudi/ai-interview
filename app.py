import streamlit as st
import pandas as pd
import sqlite3
from database.initdb import initinterviewdatabase
from utils.audio import verifyandtranscribeaudio

st.set_page_config(page_title="AI Interview Platform", layout="wide")
st.title("🎙️ Local Agentic AI Interview Platform")

st.sidebar.header("Phase 1: Candidate Baseline")
candidatename = st.sidebar.text_input("Candidate Name", "John Doe")
difficulty = st.sidebar.slider("Baseline Question Difficulty", 1, 5, 3)
resumetext = st.sidebar.text_area("Paste Resume Text")
jobtext = st.sidebar.text_area("Paste Job Description")

if st.sidebar.button("Initialize Platform Database"):
    initinterviewdatabase()
    st.sidebar.success("Database Ready!")

st.header("Current Interview Step")
currentquestion = "Can you describe a time you optimized a database configuration for concurrent writes?"
st.info(f"**Question:** {currentquestion}")

st.subheader("Phase 3: Capture Response")
mockfilepath = st.text_input("Audio File Path (e.g., response.wav)", "response.wav")

if st.button("Submit Verbal Answer"):
    validation = verifyandtranscribeaudio(mockfilepath)
    
    if not validation["passed"]:
        st.error(f"⚠️ Validation Failed: {validation['message']}")
        st.warning(f"Your word count: {validation['count']} words. Minimum required: 10 words.")
    else:
        st.success(f"✅ {validation['message']}")
        st.write(f"**Transcript:** {validation['text']}")
        
        conn = sqlite3.connect("interviewapp.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO evaluations 
            (evaluationid, questionid, techscore, commscore, wpm, verifierscore, perfectedphrase, quizpassed)
            VALUES ('e1', 'q1', 85.0, 60.0, 145, 95.0, 'To optimize the database, I implemented a WAL setup...', 1)
        """)
        conn.commit()
        conn.close()

st.divider()
st.header("Phase 6: Performance Scoreboard")

try:
    conn = sqlite3.connect("interviewapp.db")
    df = pd.read_sql_query("SELECT techscore, commscore, wpm, verifierscore FROM evaluations", conn)
    conn.close()
    
    if not df.empty:
        latest = df.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Technical Depth", value=f"{latest['techscore']}/100")
        col2.metric(label="STAR Communication", value=f"{latest['commscore']}/100", delta="+15.0 After Quiz Gate")
        col3.metric(label="Pacing Speed", value=f"{int(latest['wpm'])} WPM")
        col4.metric(label="Resume Verification", value=f"{latest['verifierscore']}/100")
    else:
        st.info("No evaluation scores recorded yet. Submit an accepted answer to see metrics.")
except Exception as e:
    st.info("Click 'Initialize Platform Database' in the sidebar to sync scoreboard tables.")
