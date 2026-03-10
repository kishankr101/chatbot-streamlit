import streamlit as st

st.title("🤖 Kishan AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask something")

def bot_reply(text):
    text = text.lower()

    if "hello" in text:
        return "Hello! Nice to meet you."
    elif "ai" in text:
        return "AI means Artificial Intelligence."
    elif "finance" in text:
        return "Finance is about money, investments and budgeting."
    elif "your name" in text:
        return "I am Kishan's chatbot."
    else:
        return "I am still learning. Ask something else."

if user_input:
    response = bot_reply(user_input)

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", response))

for sender, msg in st.session_state.messages:
    st.write(f"**{sender}:** {msg}")
