import streamlit as st

def render_question_form():
    st.subheader("Ask a Question")
    with st.form("question_form"):
        question = st.text_area("Your question:", placeholder="Ask anything about your studies...")
        subject = st.selectbox("Subject:", ["Math", "Science", "History", "Literature", "Other"])
        submitted = st.form_submit_button("Get Answer")
        return question, subject, submitted
