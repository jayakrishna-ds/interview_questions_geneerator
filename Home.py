import streamlit as st
from resume_parser import parse_resume

st.set_page_config(page_title="Resume Upload", layout="centered")

st.markdown("""
            <style>
            [data-testid="stSidebar"]{ display:none;}
            """, unsafe_allow_html=True)

st.title="Home"
st.markdown("### Upload your resume to begin")

uploaded_file=st.file_uploader(
    "Upload your Resume (PDF or DOCX)",
    type=["pdf","docx"]
)

if uploaded_file:
    if "resume_text" not in st.session_state:
        resume_text=parse_resume(uploaded_file)

        if not resume_text.strip():
            st.error("Unable to extract text from resume.")
            st.stop()

        st.session_state["resume_text"]=resume_text
        st.success("Resume uploaded sucessfully!")


if "resume_text" in st.session_state:
    st.markdown("## What do you want to do next?")

    col1,col2=st.columns(2)

    with col1:
        if st.button("Resume Analyzer",use_container_width=True):
            st.switch_page("pages/1_resume_analyzer.py")
    
    with col2:
        if st.button("Interview Questions",use_container_width=True):
            st.switch_page("pages/2_Interview_Questions.py")

else:
    st.info("Upload a Resume")