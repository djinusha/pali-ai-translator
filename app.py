import streamlit as st
import google.generativeai as genai
from streamlit_antd_components import button # මෙය අවශ්‍ය නැත, අපි සරලව සාදමු

# පිටුවේ සැකසුම්
st.set_page_config(page_title="AI පාලි පරිවර්තකය", page_icon="☸️")

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']:
            if preferred in available_models:
                return preferred
        return available_models[0] if available_models else None
    except:
        return None

# API සම්බන්ධතාවය
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model_id = get_working_model()
    model = genai.GenerativeModel(model_id) if model_id else None

st.title("☸️ AI පාලි පරිවර්තකය")
st.markdown("---")

# --- පාලි විශේෂ අකුරු පුවරුව (Pali Keyboard) ---
st.write("විශේෂ අකුරු අවශ්‍ය නම් මෙතැනින් තෝරන්න:")
special_chars = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ṇḍ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ']
cols = st.columns(len(special_chars))

# session_state භාවිතා කර ටයිප් කරන දේ තබා ගැනීම
if 'pali_input' not in st.session_state:
    st.session_state.pali_input = ""

def add_char(char):
    st.session_state.pali_input += char

for i, char in enumerate(special_chars):
    if cols[i].button(char):
        add_char(char)

# පාලි වාක්‍යය ඇතුළත් කරන කොටුව
pali_text = st.text_area("පාලි වාක්‍යය මෙහි ඇතුළත් කරන්න:", value=st.session_state.pali_input, key="main_input")

# Clear බොත්තම
if st.button("පිරිසිදු කරන්න (Clear)"):
    st.session_state.pali_input = ""
    st.rerun()

st.markdown("---")

if st.button("පරිවර්තනය කරන්න", type="primary"):
    if pali_text:
        with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
            try:
                prompt = f"As a Pali scholar, translate this to Sinhala and English with word meanings: {pali_text}"
                response = model.generate_content(prompt)
                st.markdown("### 📝 ප්‍රතිඵලය:")
                st.write(response.text)
            except Exception as e:
                st.error(f"පරිවර්තනය අසාර්ථක විය: {e}")
    else:
        st.warning("කරුණාකර පාලි වාක්‍යයක් ඇතුළත් කරන්න.")
