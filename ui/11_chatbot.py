import streamlit as st
from api.chat import generate_chat_response
from app import page_header

st.set_page_config(page_title="Career AI Assistant", page_icon="💬", layout="wide")

page_header("AI Advisory", "Career Assistant", "Chat with our context-aware agent for instantaneous salary data, career path advice, and high-ROI skill recommendations.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to use the AI Assistant.")
    st.stop()

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": f"Hi {st.session_state.username}! I am your AI Career Advisor. You can ask me about salary bands for specific roles, skill development, or how to negotiate promotions."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g: What skills do I need to be an ML Engineer?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
    # Get conversational logic from the backend service directly
    response = generate_chat_response(prompt, st.session_state.chat_messages)
    
    # Display assistant logic
    with st.chat_message("assistant"):
        st.markdown(response)
        
    # Update state
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
