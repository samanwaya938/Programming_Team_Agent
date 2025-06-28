import streamlit as st
from langchain_core.messages import HumanMessage
from agent import graph  # Make sure agent.py defines and exposes `graph`

# Page settings
st.set_page_config(page_title="Programming Team Agent", layout="wide")

st.title("👨‍💻 Programming Team Agent")
st.write("Enter your programming query below. Your virtual software team will handle the request through all 7 expert agents.")

# User input
user_input = st.text_area("💬 Your Query", placeholder="e.g. Build a REST API in Python to manage tasks with authentication.")

if st.button("🚀 Run"):
    if user_input.strip() == "":
        st.warning("Please enter a programming query.")
    else:
        with st.spinner("Agents are working..."):
            result = graph.invoke({"messages": [HumanMessage(content=user_input)]})

        # Display outputs for each agent
        st.subheader("🧠 Analyst")
        st.code(result['messages'][-7].content, language='markdown')

        st.subheader("📐 Architect")
        st.code(result['messages'][-6].content, language='markdown')

        st.subheader("💻 Developer")
        st.code(result['messages'][-5].content, language='python')

        st.subheader("🧹 Reviewer")
        st.code(result['messages'][-4].content, language='markdown')

        st.subheader("✅ Tester")
        st.code(result['messages'][-3].content, language='markdown')

        st.subheader("🗂️ Diagram Creator")
        st.code(result['messages'][-2].content, language='markdown')

        st.subheader("📝 Summarizer")
        st.code(result['messages'][-1].content, language='markdown')
