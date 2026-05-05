import streamlit as st
import google.generativeai as genai

# Gemini Setup - 'gemini-1.5-flash-latest' use karein
genai.configure(api_key="AIzaSyD7-Z5X-cPGtODt5drBDAdllybhnEP3AiI") 
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="AK Assistant", page_icon="🤖")
st.title("🤖 AK Assistant")
st.caption("Alok Kumar's Personal AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bol Alok, kya kaam hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Tumhara naam AK hai. Alok Kumar ke best friend ho. Desi Hindi mein iska jawab do: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Opps! Kuch gadbad ho gayi: {e}")
            
