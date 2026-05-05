import streamlit as st
import google.generativeai as genai

# API Key configure karein
API_KEY = "AIzaSyD7-Z5X-cPGtODt5drBDAdllybhnEP3AiI"
genai.configure(api_key=API_KEY)

# --- AUTO MODEL SELECTOR ---
def select_best_model():
    try:
        # Ye line Google se saare available models ki list mangwayegi
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Hum sabse naya (Flash 1.5) dhundhne ki koshish karenge, warna jo pehla milega wo le lenge
        for name in available_models:
            if 'gemini-1.5-flash' in name:
                return name
        return available_models[0] # Agar flash nahi mila toh list ka pehla model
    except Exception:
        return "gemini-1.5-flash" # Backup agar list na mil paye

# Model select karna
if "model_name" not in st.session_state:
    st.session_state.model_name = select_best_model()

model = genai.GenerativeModel(st.session_state.model_name)

# --- Streamlit UI ---
st.title("🤖 AK Assistant")
st.caption(f"Active Model: {st.session_state.model_name}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bol Alok, kya haal hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Best friend personality setup
            full_prompt = f"Tumhara naam AK hai. Alok Kumar ke best friend ho. Desi Hindi mein jawab do: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Locha ho gaya: {e}")
            
