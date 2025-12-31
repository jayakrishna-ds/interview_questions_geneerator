import streamlit as st

st.set_page_config(page_title="Resume Analyzer",layout="wide")

st.sidebar.title("Navigation")
st.sidebar.info("Resume Analysis Tools")

st.title="Resume Analyzer"

if "resume_text" not in st.session_state:
    st.warning("Please upload your resume first.")
    st.stop()

text=st.session_state["resume_text"].lower()

score=0
feedback=[]

if "experience" in text:
    score+=20
else:
    feedback.append("Add an experience section.")

if "project" in text:
    score+=20
else:
    feedback.append("Add projects with impact.")

if "skills" in text:
    score+=20
else:
    feedback.append("Add a skill section.")

if "education" in text:
    score+=20
else:
    feedback.append("education section is missing.")

if len(text.split())>300:
    score+=20
else:
    feedback.append("Resume content is too short.")

st.metric("Resume score out of 100", score)

st.subheader("Resume Improvement Feedback")
for f in feedback:
    st.write(f"{f}")