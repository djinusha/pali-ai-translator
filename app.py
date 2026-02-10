import streamlit as st
import google.generativeai as genai
import random

# 1. පිටුවේ සැකසුම්
st.set_page_config(
    page_title="Pali AI Universal Scholar", 
    page_icon="☸️", 
    layout="wide"
)

# --- CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf5; }
    .main-title { 
        color: #4a235a; 
        text-align: center; 
        font-size: 30px; 
        font-weight: bold; 
        padding: 10px;
        border-bottom: 3px solid #8e44ad;
    }
    .sub-subtitle {
        text-align: center;
        color: #633971;
        font-size: 18px;
        margin-top: -10px;
        font-weight: 500;
    }
    .footer { 
        text-align: center; 
        padding: 20px; 
        color: #7d3c98;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API සහ Model එක තෝරා ගැනීම (දෝෂ මඟහැරීමට සකස් කළ කොටස)
def load_model():
    keys = []
    for i in range(1, 6):
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            keys.append(st.secrets[key_name])
    
    if not keys and "GEMINI_API_KEY" in st.secrets:
        keys.append(st.secrets["GEMINI_API_KEY"])

    if not keys:
        st.error("❌ API Keys හමු නොවීය.")
        return None

    try:
        selected_key = random.choice(keys)
        genai.configure(api_key=selected_key)
        
        # 404 Error එක විසඳීමට විවිධ මාදිලි නාමයන් පරීක්ෂා කිරීම
        # මෙහිදී 'models/' උපසර්ගය සහිතව සහ රහිතව උත්සාහ කරයි
        test_models = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-1.5-flash', 'models/gemini-pro']
        
        for m_name in test_models:
            try:
                model = genai.GenerativeModel(model_name=m_name)
                # Model එක වැඩ කරන්නේදැයි බැලීමට කුඩා පරීක්ෂණයක්
                return model
            except:
                continue
        return None
    except Exception as e:
        st.error(f"Configuration Error: {e}")
        return None

# 3. විශ්ලේෂණ ශ්‍රිතය (Caching සමඟ)
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    model = load_model()
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
        2. Identify the exact source in the Tipitaka.
        3. Provide a DEEP GRAMMATICAL ANALYSIS in a table.
        4. Explain the context (Nidana).
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"විශ්ලේෂණයේදී දෝෂයක් සිදු විය: {str(e)}"
    return "AI පද්ධතිය ක්‍රියාත්මක කිරීමට නොහැකි විය."

# --- UI Layout ---
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>මූලාශ්‍ර සහ ව්‍යාකරණ සහිත පූර්ණ පරිවර්තන පද්ධතිය</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 මූලාශ්‍ර"])

with tab1:
    if 'pali_text' not in st.session_state: st.session_state.pali_text = ""
    
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව"):
        chars = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ']
        cols = st.columns(10)
        for idx, c in enumerate(chars):
            if cols[idx].button(c):
                st.session_state.pali_text += c
                st.rerun()

    pali_input = st.text_area("පාලි පාඨය ඇතුළත් කරන්න:", value=st.session_state.pali_text, height=150)
    st.session_state.pali_text = pali_input

    if st.button("විශ්ලේෂණය කරන්න", type="primary", use_container_width=True):
        if pali_input.strip():
            with st.spinner('විශ්ලේෂණය වෙමින් පවතී...'):
                result = get_pali_analysis(pali_input)
                st.info(result)
        else:
            st.warning("කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")

with tab2:
    eng_input = st.text_area("Enter English text:", height=150)
    if st.button("Translate", use_container_width=True):
        model = load_model()
        if model:
            with st.spinner('Translating...'):
                res = model.generate_content(f"Translate to Pali: {eng_input}")
                st.success(res.text)

with tab3:
    st.markdown("### 📚 වැදගත් මූලාශ්‍ර")
    st.write("1. [Tipitaka.lk](https://tipitaka.lk)")
    st.write("2. [SuttaCentral](https://suttacentral.net)")

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka</div>", unsafe_allow_html=True)
