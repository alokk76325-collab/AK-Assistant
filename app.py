import streamlit as st
import requests
import os
from groq import Groq

# --- API Setup (SECURE) ---
# Ab code key ko Render ke Environment Variables se uthayega
API_KEY = os.getenv("GROQ_API_KEY") 
client = Groq(api_key=API_KEY)

# --- APP CONFIG ---
st.set_page_config(page_title="AK Assistant", page_icon="🤖")
st.title("🤖 AK Ultimate System")

# Memory aur Mode ko save rakhne ke liye Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bol bhai Alok! Abhi main Fast Mode ⚡ mein chal raha hoon."}]
if "active_model" not in st.session_state:
    st.session_state.active_model = "llama-3.1-8b-instant"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": "Tumhara naam AK hai. Tum Alok ke personal assistant ho. Desi hindi mein baat karo. Jawab chhote aur point par do."}]

# --- AUTO LOCATION TRACKER ---
def get_my_city():
    try:
        res = requests.get("http://ip-api.com/json/", timeout=3)
        return res.json()['city']
    except:
        return "Dumri" 

# Purani chat screen par dikhane ke liye
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if query := st.chat_input("Aapka sandesh..."):
    # User ka message screen par dikhao
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    query_lower = query.lower().strip()

    response_text = ""

    # --- MODE SWITCHING ---
    if query_lower == "pro mode":
        st.session_state.active_model = "llama-3.3-70b-versatile"
        response_text = "System upgraded! Ab main Pro Mode 🧠 mein gahrai se soch kar jawab dunga."
        
    elif query_lower == "fast mode":
        st.session_state.active_model = "llama-3.1-8b-instant"
        response_text = "System switched! Ab Fast Mode ⚡ mein replies goli ki tarah aayenge."

    # --- LOCATION ---
    elif "location" in query_lower or "kahan hoon" in query_lower:
        city = get_my_city()
        response_text = f"Bhai, tumhari location ka link neeche hai:\n\n[📍 Click karke Map kholo](http://maps.google.com/maps?q=my+current+location)"

    # --- WEATHER ---
    elif "weather" in query_lower or "mausam" in query_lower or "wether" in query_lower:
        city = query_lower.replace("weather", "").replace("wether", "").replace("mausam", "").replace("ka", "").replace("batao", "").strip()
        if not city:
            city = get_my_city() 
        response_text = f"Bhai, {city} ka mausam yahan check kar lo:\n\n[🌤️ Click for {city} Weather](https://www.google.com/search?q=weather+{city})"

    # --- CALLS ---
    elif "call" in query_lower:
        person = query_lower.replace("call", "").strip()
        if person.isdigit():
            response_text = f"[📞 Click karke {person} ko Call lagao](tel:{person})"
        else:
            response_text = f"Bhai, {person} ka number bata do."

    # --- YOUTUBE ---
    elif "youtube" in query_lower or "play" in query_lower or "gaana" in query_lower or "song" in query_lower:
        song = query_lower.replace("youtube", "").replace("pr", "").replace("par", "").replace("chalao", "").replace("lagao", "").replace("play", "").replace("song", "").replace("gaana", "").strip()
        if song:
            response_text = f"Bhai, '{song}' ka YouTube link ready hai:\n\n[▶️ Click karke YouTube par chalao](https://www.youtube.com/results?search_query={song})"
        else:
            response_text = "Kaunsa gaana lagau bhai? Naam toh batao!"

    # --- AI CHAT (Groq API) ---
    else:
        try:
            st.session_state.chat_history.append({"role": "user", "content": query})
            
            completion = client.chat.completions.create(
                model=st.session_state.active_model,
                messages=st.session_state.chat_history,
                temperature=0.7,
            )
            response_text = completion.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        except Exception as e:
            response_text = "Bhai thoda network issue aa gaya hai ya API Key set nahi hai."
            if len(st.session_state.chat_history) > 1:
                st.session_state.chat_history.pop()

    # AK ka reply screen par dikhao aur save karo
    if response_text:
        st.chat_message("assistant").markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    
