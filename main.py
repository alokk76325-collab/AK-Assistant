import streamlit as st
import google.generativeai as genai

# --- Configuration ---
# 1. Yahan apni sahi API Key daal dena
API_KEY = "AIzaSyD7-Z5X-cPGtODt5drBDAdllybhnEP3AiI" 
genai.configure(api_key=API_KEY)

# 2. Model setup: Humne 'gemini-1.5-flash' rakha hai jo fast aur free hai
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Streamlit UI ---
st.set_page_config(page_title="AK Assistant", page_icon="🤖", layout="centered")

# Custom CSS for a better look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AK Assistant")
st.caption("Alok Kumar's Personal AI | Powered by Gemini")

# Chat History Initialize karna
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani messages display karna
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Bol Alok, kya kaam hai?"):
    # User message save aur show karna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response generate karna
    with st.chat_message("assistant"):
        try:
            # Personal touch ke liye system instruction yahan add kiya hai
            system_prompt = f"Tumhara naam AK hai. Tum Alok Kumar ke best friend ho. Desi Hindi aur thodi Hinglish mein jawab do. Sawal ye hai: {prompt}"
            
            response = model.generate_content(system_prompt)
            
            if response.text:
                full_response = response.text
                st.markdown(full_response)
                # History mein save karna
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Dost, model ne koi response nahi diya. Ek baar check kar.")
                
        except Exception as e:
            # Agar abhi bhi 404 aaye toh ye message help karega
            error_msg = str(e)
            if "404" in error_msg:
                st.error("Error: Model nahi mila. 'gemini-1.5-flash' name verify karein.")
            elif "location" in error_msg.lower():
                st.error("Error: Render ka ye server Gemini support nahi kar raha. Region badal kar dekho.")
            else:
                st.error(f"Kuch locha ho gaya: {error_msg}")
                
