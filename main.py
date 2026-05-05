import streamlit as st
import google.generativeai as genai

# Gemini Setup
genai.configure(api_key="AIzaSyD7-Z5X-cPGtODt5drBDAdllybhnEP3AiI") # Apni key check kar lena
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AK Assistant", page_icon="🤖")
st.title("🤖 AK Assistant")
st.caption("Alok Kumar's Personal AI")

# Chat History setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User se input lene ke liye (Asli Fix yahan hai)
if prompt := st.chat_input("Bol Alok, kya kaam hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI ka response
    with st.chat_message("assistant"):
        response = model.generate_content(f"Tumhara naam AK hai. Alok Kumar ke best friend ho. Desi Hindi mein iska jawab do: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
