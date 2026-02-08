import streamlit as st
import google.generativeai as genai

# 1. පිටුවේ සැකසුම්
st.set_page_config(
    page_title="AI පාලි පරිවර්තකය", 
    page_icon="☸️",
    layout="centered"
)

# --- පෙනුම ලස්සන කිරීමට CSS (Custom Styling) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #fdfaf5;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #633971;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #d1c4e9;
    }
    h1 {
        color: #4a235a;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #4a235a;
        text-align: center;
        padding: 5px;
        font-size: 14px;
        border-top: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. වැඩ කරන මාදිලියක් සොයා ගැනීම
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']:
            if preferred in available_models:
                return preferred
        return available_models[0] if available_models else None
    except:
        return None

# 3. API සම්බන්ධතාවය
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model_id = get_working_model()
    model = genai.GenerativeModel(model_id) if model_id else None
else:
    st.error("Secrets හි API Key එක හමු නොවීය.")

# 4. ශීර්ෂය
st.markdown("<h1>☸️ AI පාලි පරිවර්තකය</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7d3c98;'>ගැඹුරු පාලි අර්ථ සරලව සිංහලෙන් සහ ඉංග්‍රීසියෙන්</p>", unsafe_allow_html=True)
st.markdown("---")

# --- පාලි විශේෂ අකුරු පුවරුව ---
st.write("⌨️ **විශේෂ අකුරු පුවරුව (Pali Keyboard):**")
if 'pali_input' not in st.session_state:
    st.session_state.pali_input = ""

def add_char(char):
    st.session_state.pali_input += char

special_chars = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ṇḍ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ']
cols = st.columns(len(special_chars))
for i, char in enumerate(special_chars):
    if cols[i].button(char, key=f"btn_{char}"):
        add_char(char)

# පාලි පාඨය ඇතුළත් කරන කොටුව
pali_text = st.text_area(
    "", 
    value=st.session_state.pali_input,
    height=150,
    placeholder="පාලි වාක්‍යය මෙහි ටයිප් කරන්න හෝ ඉහත බොත්තම් භාවිතා කරන්න...",
    key="text_input_area"
)

# බොත්තම් පෙළ
col_btn1, col_btn2 = st.columns([4, 1])
with col_btn1:
    translate_btn = st.button("පරිවර්තනය කරන්න", type="primary")
with col_btn2:
    if st.button("Clear"):
        st.session_state.pali_input = ""
        st.rerun()

st.markdown("---")

# 5. ප්‍රතිඵලය පෙන්වීම
if translate_btn:
    if pali_text:
        with st.spinner('AI මගින් අර්ථ විශ්ලේෂණය කරමින් පවතී...'):
            try:
                prompt = f"You are a Pali scholar. Translate this to Sinhala and English. Provide a word-by-word meaning table: {pali_text}"
                response = model.generate_content(prompt)
                st.markdown("### 📝 පරිවර්තනය සහ අර්ථ විවරණය:")
                st.info(response.text)
            except Exception as e:
                st.error(f"දෝෂයක් සිදු විය: {e}")
    else:
        st.warning("කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")

# --- ඔබගේ නම ඇතුළත් කළ Footer එක ---
st.markdown("""
    <div class="footer">
        <p>Created by Jinusha Dissanayaka | Powered by Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
