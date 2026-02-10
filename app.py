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
    .resource-link {
        background-color: #f4ecf7;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #8e44ad;
        margin: 5px 0px;
    }
    .footer { 
        position: relative;
        text-align: center; 
        padding: 20px; 
        color: #7d3c98;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API Keys සහ Model තෝරා ගැනීම (Error Handling සමඟ)
def load_model():
    # Secrets තුළ ඇති Keys සොයා ගැනීම
    keys = []
    for i in range(1, 6):
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            keys.append(st.secrets[key_name])
    
    if not keys and "GEMINI_API_KEY" in st.secrets:
        keys.append(st.secrets["GEMINI_API_KEY"])

    if not keys:
        st.error("❌ API Keys කිසිවක් හමු නොවීය. කරුණාකර Secrets පරීක්ෂා කරන්න.")
        return None

    selected_key = random.choice(keys)
    genai.configure(api_key=selected_key)

    # 404 දෝෂය මඟහරවා ගැනීමට නිවැරදි මාදිලි නාමයන් පරීක්ෂා කිරීම
    # models/gemini-1.5-flash වෙනුවට gemini-1.5-flash ලෙස භාවිතය වඩාත් සුදුසුයි
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            # කුඩා පරීක්ෂණයක් (Test request එකක් නොයවා සරලව model එක return කරයි)
            return model
        except:
            continue
    return None

model = load_model()

# 3. AI ප්‍රතිචාර ලබා ගැනීම (Caching සමඟ)
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
        2. Identify the exact source in the Tipitaka.
        3. Provide a DEEP GRAMMATICAL ANALYSIS (Padavigga) in a table.
        4. List relevant references to SuttaCentral.net or Tipitaka.lk.
        5. Explain the context (Nidana).
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI ප්‍රතිචාරයේ දෝෂයකි: {str(e)}"
    return "AI මාදිලිය සක්‍රීය නැත."

# 4. Interface Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, ව්‍යාකරණ සහ මූලාශ්‍ර සහිත පූර්ණ පද්ධතිය</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

with tab1:
    if 'pali_text' not in st.session_state: st.session_state.pali_text = ""
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}"):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("Pali Text:", value=st.session_state.pali_text, height=150)
    st.session_state.pali_text = pali_input

    if st.button("Analyze Pali", type="primary", use_container_width=True):
        if pali_input.strip():
            with st.spinner('විශ්ලේෂණය කරමින් පවතී...'):
                result = get_pali_analysis(pali_input)
                st.markdown("### 📖 ප්‍රතිඵලය:")
                st.info(result)

with tab2:
    eng_input = st.text_area("Enter English text:", height=150)
    if st.button("Translate to Pali", type="primary"):
        if eng_input.strip() and model:
            with st.spinner('Translating...'):
                response = model.generate_content(f"Translate to Classical Pali: {eng_input}")
                st.success(response.text)

with tab3:
    st.markdown("### 📚 පාලි සම්පත්")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">සූත්‍ර එකතුව</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
