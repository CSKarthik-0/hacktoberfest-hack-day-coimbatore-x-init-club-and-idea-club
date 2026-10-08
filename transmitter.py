import streamlit as st
from google import genai
import requests

# --- 1. CONFIGURATION ---
# Replace with your actual Google AI Studio API Key
API_KEY = ""

# Initialize Google's AI Studio SDK
client = genai.Client(api_key=API_KEY)

# Primary Gemma 4 Model ID on Google AI Studio
GEMMA_4_MODEL = "gemma-4-26b-a4b-it"  # Alternatively: "gemma-4-31b-it"

# Replace with Laptop B's actual IPv4 address
LAPTOP_B_IP = "172.20.10.2" 
BASE_STATION_URL = f"http://{LAPTOP_B_IP}:5000/receive"

# --- 2. INTERFACE ---
st.title("📱 Field Unit (Laptop A)")
st.subheader("Engine: Pure Gemma 4")

user_input = st.text_area("Incident Report:", height=150)

if st.button("Compress & Transmit"):
    if user_input.strip():
        with st.spinner("Gemma 4 is compressing telemetry..."):
            prompt = f"""
            You are an edge telemetry compressor for disaster mesh networks.
            If the message is an emergency, extract facts into this exact format:
            PRIO:<CRITICAL/HIGH>|LOC:<Location>|HAZ:<Hazard>|CAS:<Count>|REQ:<NeededResources>
            Output ONLY the formatted string without extra text.
            
            Input: {user_input}
            """
            
            try:
                # Call Gemma 4
                response = client.models.generate_content(
                    model=GEMMA_4_MODEL,
                    contents=prompt
                )
                telemetry = response.text.strip()
                
                st.success("Compression Complete!")
                st.code(telemetry, language="text")
                
                # Send to Laptop B
                req = requests.post(BASE_STATION_URL, json={"packet": telemetry}, timeout=5)
                if req.status_code == 200:
                    st.success("Transmitted to Base Station over local mesh!")
                else:
                    st.warning(f"Base Station returned code {req.status_code}")
            except Exception as e:
                st.error(f"Gemma 4 Error: {e}")
    else:
        st.warning("Please type a message first.")