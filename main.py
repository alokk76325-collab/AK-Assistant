import streamlit as st
import google.generativeai as genai

# API Key configure karein
# (Apni original key use karna jo tumhare paas hai)
API_KEY = "AIzaSyD7-Z5X-cPGtODt5drBDAdllybhnEP3AiI" 
genai.configure(api_key=API_KEY)

# --- AUTO MODEL SELECTOR (FIXED PREFIX ISSUE) ---
def select_best_model():
    try:
        # Google se saare models ki full list mangwayein (ye 'models/' prefix ke saath hoti hai)
        raw_available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Hum prefix hata kar sirf 'gemini-1.5-flash' ya 'gemini-1.5-pro' dundhein ge
        clean_model_names = [name.split('/')[-1] for name in raw_available_models]

        # Hum sabse pehle 'gemini-1.5-flash' dhundhenge (sabse fast aur free)
        for name in clean_model_names:
            if 'gemini-1.5-flash' == name:
                return name
        
        # Agar flash nahi mila toh 'gemini-1.5-pro' try karenge
        for name in clean_model_names:
            if 'gemini-1.5-pro' == name:
                return name
        
        # Agar koi specific model nahi mila toh list ka pehla clean name use karenge
        return clean_model_names[0]
    except Exception:
        # Backup: directly provide the most likely working model name
        return "gemini-1.5-flash"

# Model select karna
if "model_name" not in st.session_state:
    st.session_state.model_name = select_best_model()

# Final model initialization
model = genai.GenerativeModel(st.session_state.model_name)

# --- Streamlit UI ---
st.title("🤖 AK Assistant")
# Updated title to show actual active model name
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
            # Better error message
            st.error(f"Dost, model '{st.session_state.model_name}' connect nahi ho pa raha: {e}")
            
