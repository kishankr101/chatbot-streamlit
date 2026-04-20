import os
import streamlit as st
from openai import OpenAI

# =========================
# Page setup
# =========================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Custom CSS for better UI
# =========================
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
            color: white;
        }

        .stApp {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        }

        .title-box {
            padding: 1.2rem 1.4rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            margin-bottom: 1rem;
        }

        .title-box h1 {
            margin: 0;
            font-size: 2.1rem;
            font-weight: 800;
            color: white;
        }

        .title-box p {
            margin: 0.35rem 0 0 0;
            color: #cbd5e1;
            font-size: 1rem;
        }

        .card {
            padding: 1rem;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.10);
            margin-bottom: 0.8rem;
        }

        .stChatMessage {
            border-radius: 14px;
            padding: 0.2rem 0;
        }

        section[data-testid="stSidebar"] {
            background: #0b1220;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        .small-note {
            color: #94a3b8;
            font-size: 0.9rem;
        }

        .footer-note {
            text-align: center;
            color: #94a3b8;
            margin-top: 1rem;
            font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# API key
# =========================
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
if not api_key:
    st.error("Please set your OPENAI_API_KEY in Streamlit secrets or environment variables.")
    st.stop()

client = OpenAI(api_key=api_key)

# =========================
# Session state
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "gpt-4.1-mini"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("## 🤖 AI Chatbot")
    st.markdown("A clean, modern chatbot with chat memory and better responses.")

    st.session_state.model = st.selectbox(
        "Model",
        ["gpt-4.1-mini", "gpt-4.1", "gpt-4o-mini"],
        index=0
    )

    st.session_state.temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    st.markdown("---")
    st.markdown("### Quick prompts")
    quick_prompts = [
        "Explain Python in simple words",
        "Give me 5 project ideas for students",
        "Write a professional email",
        "Help me debug this code"
    ]

    for prompt in quick_prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="small-note">
        Tip: Use the chat like a normal conversation.  
        The assistant will remember the conversation in this session.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# Header
# =========================
st.markdown(
    """
    <div class="title-box">
        <h1>🤖 AI Chatbot</h1>
        <p>Ask anything. Get smart, contextual, and helpful answers.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# System prompt
# =========================
SYSTEM_PROMPT = """
You are a helpful, friendly, and intelligent AI assistant.
Answer clearly, accurately, and in a conversational style.
If the user asks for code, provide clean and practical code.
If the user asks follow-up questions, use the previous chat context.
If something is unclear, ask a short clarifying question.
"""

# =========================
# Show chat history
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# Helper: get assistant response
# =========================
def get_ai_response(messages):
    response = client.responses.create(
        model=st.session_state.model,
        instructions=SYSTEM_PROMPT,
        input=messages,
        temperature=st.session_state.temperature,
    )

    # Safer text extraction
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    try:
        return response.output[0].content[0].text
    except Exception:
        return "Sorry, I could not generate a response."

# =========================
# Chat input
# =========================
user_input = st.chat_input("Type your message...")

if user_input:
    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                ai_reply = get_ai_response(st.session_state.messages)
                st.markdown(ai_reply)
            except Exception as e:
                ai_reply = f"⚠️ Error: {e}"
                st.error(ai_reply)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# =========================
# Footer
# =========================
st.markdown(
    """
    <div class="footer-note">
        Built with Streamlit + OpenAI
    </div>
    """,
    unsafe_allow_html=True,
)
