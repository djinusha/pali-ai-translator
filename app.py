import streamlit as st
import google.generativeai as genai

# 1. පිටුවේ සැකසුම්
st.set_page_config(page_title="Pali AI Universal Scholar", page_icon="☸️", layout="wide")

# --- CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf5; }
    .main-title { color: #4a235a; text-align: center; font-size: 32px; font-weight: bold; border-bottom: 3px solid #8e44ad; padding-bottom: 10px; }
    .grammar-box { background-color: #fcf3cf; padding: 15px; border-radius: 10px; border-left: 5px solid #f1c40f; }
    .footer { text-align: center; padding: 20px; color: #7d3c98; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. API සහ Model එක තෝරා ගැනීම
def load_model():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            preferred_models = ['models/gemini-1.5-flash', 'models/gemini-pro']
            selected_model = next((m for m in preferred_models if m in available_models), available_models[0])
            return genai.GenerativeModel(selected_model)
        except Exception: return None
    return None

model = load_model()

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>ගැඹුරු ව්‍යාකරණ විශ්ලේෂණය සහ මූලාශ්‍ර සහිතයි</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

# --- Tab 1: පාලි සිට අනෙක් භාෂාවලට (ගැඹුරු ව්‍යාකරණ සමඟ) ---
with tab1:
    st.subheader("පාලි විශ්ලේෂණය (Translation & Deep Grammar)")
    
    if 'pali_text' not in st.session_state: st.session_state.pali_text = ""

    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("Pali Text:", value=st.session_state.pali_text, height=150, placeholder="ගාථාවක් හෝ පාලි පාඨයක් මෙහි යොදන්න...")
    st.session_state.pali_text = pali_input

    if st.button("විශ්ලේෂණය ආරම්භ කරන්න", type="primary", use_container_width=True):
        if pali_input and model:
            with st.spinner('ව්‍යාකරණ සහ මූලාශ්‍ර පරීක්ෂා කරමින් පවතී...'):
                # AI එකට දෙන ඉතා ගැඹුරු උපදෙස් (Deep Grammar Prompt)
                prompt = f"""
                As a world-class Pali Grammarian and Philologist:
                1. Translate this Pali text into Sinhala and English: "{pali_input}"
                2. Identify the Tipitaka source (Nikaya/Sutta/Verse).
                3. Provide a DEEP GRAMMATICAL ANALYSIS for each word:
                   - Root (Dhatu)
                   - Case (Vibhakti) for nouns or Tense/Mood for verbs
                   - Gender (Linga) and Number (Vacana)
                   - Sandhi or Samasa (if applicable)
                4. Explain any complex grammatical structures used.
                5. Provide direct source URLs (Tipitaka.lk, SuttaCentral).
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown("### 📖 සම්පූර්ණ විවරණය:")
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි (ව්‍යාකරණ උපදෙස් සමඟ) ---
with tab2:
    st.subheader("English to Pali (Grammar Guided)")
    eng_input = st.text_area("Enter English text:", height=150)
    
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input and model:
            with st.spinner('පාලි භාෂාවට හරවමින් පවතී...'):
                prompt = f"""
                1. Translate to Classical Pali: "{eng_input}"
                2. Provide a detailed grammatical explanation of why those specific Pali words and case endings were used.
                3. Suggest related Pali grammar rules (e.g., Kaccayana or Moggalana).
                """
                try:
                    response = model.generate_content(prompt)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# Tab 3: මූලාශ්‍ර
with tab3:
    st.markdown("### 📚 පර්යේෂණ මෙවලම්")
    st.markdown("""
    - **Tipitaka.lk:** ත්‍රිපිටකයේ පාලි සහ සිංහල පාඨ සංසන්දනයට.
    - **SuttaCentral:** ලොව පුරා භාෂා රැසකින් සූත්‍ර කියවීමට.
    - **Pali Grammar Guide:** කච්චායන සහ මොග්ගල්ලාන ව්‍යාකරණ මූලධර්ම.
    """)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Deep Pali Grammar Engine</div>", unsafe_allow_html=True)
