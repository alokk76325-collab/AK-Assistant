import google.generativeai as genai
import webbrowser
import os

# --- API Setup ---
API_KEY = "AIzaSyD7-Z5X-cPGtODt5drBDAdllybhnEP3AiI"
genai.configure(api_key=API_KEY)

# Dynamic Model Finder
try:
    available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    active_model_name = available_models[0].name
except:
    active_model_name = "models/gemini-1.5-flash"

model = genai.GenerativeModel(
    model_name=active_model_name,
    system_instruction="Tumhara naam AK hai. Tum Alok ke personal assistant ho. Desi hindi mein baat karo."
)
chat = model.start_chat(history=[])

print(f"--- AK Ultimate System Active ---")
print("AK: Bol bhai Alok! Ab gaana ho ya location, tera bhai direct action lega.\n")

while True:
    query = input("Aap: ").lower()
    if query in ['exit', 'bye', 'so jao']: break

    # --- 1. SMART YOUTUBE SEARCH (Sabse Pehle) ---
    if "youtube" in query or "play" in query or "gaana" in query or "song" in query:
        # Faltu words hatana taaki sirf gaane ka naam bache
        song = query.replace("youtube", "").replace("pr", "").replace("par", "").replace("chalao", "").replace("lagao", "").replace("play", "").replace("song", "").replace("gaana", "").strip()
        if song:
            print(f"AK: Theek hai bhai, YouTube par '{song}' dhundh raha hoon...")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        else:
            print("AK: Kaunsa gaana bhai? Naam toh batao!")
            webbrowser.open("https://www.youtube.com")
        continue

    # --- 2. LIVE LOCATION & WEATHER ---
    if "location" in query or "kahan hoon" in query:
        print("AK: Maps khul raha hai, apni location dekh lo!")
        webbrowser.open("http://maps.google.com/maps?q=my+current+location")
        continue

    if "weather" in query or "mausam" in query:
        city = query.replace("weather", "").replace("mausam", "").replace("ka", "").strip()
        print(f"AK: Mausam ka haal hazir hai...")
        webbrowser.open(f"https://www.google.com/search?q=weather+{city if city else 'current+location'}")
        continue

    # --- 3. CALLS ---
    if "call" in query:
        person = query.replace("call", "").strip()
        webbrowser.open(f"tel:{person}") if person.isdigit() else print(f"AK: {person} ka number dalo:")
        continue

    # --- AI CHAT (Agar upar ka kuch match na ho) ---
    try:
        response = chat.send_message(query)
        print(f"AK: {response.text}")
    except Exception as e:
        print(f"AK: Error: {e}")
