import streamlit as st
import google.generativeai as genai
import os

api_key = "AIzaSyD7-Z5X-cPGtODt5drBDAdllybhnEP3AiI"

genai.configure(api_key=api_key)

# Model name fix: 'gemini-1.5-flash'
model = genai.GenerativeModel('gemini-1.5-flash')

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
            full_prompt = f"Tumhara naam AK hai. Alok Kumar ke best friend ho. Desi Hindi mein iska jawab do: {prompt}"
            response = model.generate_content(full_prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Model ne koi jawab nahi diya. Safety filters check karein.")
                
        except Exception as e:
            # Isse tumhe screen par asli error dikhega ki dikkat kahan hai
            st.error(f"Dost, kuch locha ho gaya: {e}")
            
