import streamlit as st

def render_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📚 AI Study Partner")
    with col2:
        st.write("")
