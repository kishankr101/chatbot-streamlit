import streamlit as st
from openai import OpenAI

# 🔑 Add your OpenAI API Key here
client = OpenAI(api_key="YOUR_API_KEY")

# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Title
st.title("🤖 AI Chatbot")
st.write("Ask anything and get smart answers!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=user_input
            )
            reply = response.output[0].content[0].text
            st.markdown(reply)

    # Store AI response
    st.session_state.messages.append({"role": "assistant", "content": reply})
