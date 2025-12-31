import streamlit as st
from questions_genrator import extract_skills, generate_questions
from llm_followups import generate_followups

st.set_page_config(
    page_title="AI Interview Question Generator",
    layout="wide"
)

st.sidebar.title("Interview Panel")
st.sidebar.write("Skills detected from resume")

skills=extract_skills(st.session_state["resume_text"])
for skill in skills:
    st.sidebar.markdown(f"- {skill}")
st.tile="AI Interview Questions Generator"

st.markdown("""
            <style>
            html,body,[class*="css"]{
            font-family:"Inter","Segoe UI",sans-serif;
            }

            .skill-title{
                border-left:6px;
                padding-left:12px;
                margin-top:30px;
            }

            .question-box{
                background: #f8fafc;
                border-left:6px solid #2563eb;
                padding:16px;
                border-radius:10px;
                }
            
            .answer-box{
                background:#ecfeff;
                border-left:6px solid #06b6d4;
                padding:16px;
                border-radius:10px;
            }
            
            .followup-box{
                background: #eef2ff;
                border-left: 5px solid #6366f1;
                padding: 12px;
                border-radius: 8px;
                margin-left:25px;
                }
            </style>
            """, unsafe_allow_html=True)

if "resume_text" not in st.session_state:
    st.warning("Please upload your resume to the main page first.")
    st.stop()

if not skills:
    st.warning("No skills detected in the resume.")
    st.stop()

if "questions" not in st.session_state:
    st.session_state["questions"]=generate_questions(skills)

if "ai_data" not in st.session_state:
    st.session_state["ai_data"]={}

questions=st.session_state["questions"]

if st.button("Refresh Questions"):
    st.session_state["questions"]=generate_questions(skills)
    st.session_state["ai_data"]={}
    st.rerun()

for skill,qs in questions.items():
    st.subheader(skill.upper())

    for q in qs:
        key=(skill,q)

        st.markdown(
            f"""
            <div class="question-box">
                <b>Q:</b>{q}
            </div>""",
            unsafe_allow_html=True
        )
        if st.button("Generate AI Answer", key=f"gen_{skill}_{hash(q)}"):
            with st.spinner("Generating..."):
                st.session_state["ai_data"][key]=generate_followups(skill,q)
            st.rerun()      

        if key in st.session_state["ai_data"]:
            data=st.session_state["ai_data"][key]

            st.markdown(
                f"<div class='answer-box'><b>AI Answer</b></div>",
                unsafe_allow_html=True
            )
            for p in data["answer_points"]:
                st.markdown(f"**→** {p}")

            st.markdown("**Follow-up Questions:**")
            for i,fu in enumerate(data["followups"],1):
                st.markdown(
                f"<div class='followup-box'><b>{i}.</b>{fu}</div>",
                unsafe_allow_html=True
            )
            
        st.divider()