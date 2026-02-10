import streamlit as st
import google.generativeai as genai
import random

# 1. පිටුවේ සැකසුම් (Page Settings)
st.set_page_config(
    page_title="Pali AI Universal Scholar", 
    page_icon="☸️", 
    layout="wide"
)

# --- CSS Styling (Interface එක අලංකාර කිරීමට) ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf5; }
    .main-title { 
        color: #4a235a; 
        text-align: center; 
        font-size: 32px; 
        font-weight: bold; 
        padding: 15px;
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
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #8e44ad;
        margin: 8px 0px;
        font-weight: bold;
    }
    .footer { 
        text-align: center; 
        padding: 25px; 
        color: #7d3c98;
        font-weight: bold;
        border-top: 1px solid #e1d5e7;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API Keys සහ Model එක තෝරා ගැනීම (Key Rotation)
def load_model():
    # Secrets තුළ ඇති Keys සොයා ගැනීම (GEMINI_API_KEY_1, 2, 3...)
    keys = []
    for i in range(1, 6):
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            keys.append(st.secrets[key_name])
    
    if not keys and "GEMINI_API_KEY" in st.secrets:
        keys.append(st.secrets["GEMINI_API_KEY"])

    if not keys:
        st.error("❌ API Keys කිසිවක් හමු නොවීය. කරුණාකර Streamlit Secrets පරීක්ෂා කරන්න.")
        return None

    try:
        # අහඹු ලෙස එක් Key එකක් තෝරා ගැනීම
        selected_key = random.choice(keys)
        genai.configure(api_key=selected_key)
        
        # 404 දෝෂය මඟහරවා ගැනීමට වඩාත් සුදුසු මාදිලිය තෝරා ගැනීම
        # flash වැඩ නැතිනම් pro මාදිලියට මාරු වේ
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
        for m_name in models_to_try:
            try:
                model = genai.GenerativeModel(m_name)
                return model
            except:
                continue
        return None
    except Exception as e:
        st.error(f"පද්ධතිය සැකසීමේ දෝෂයකි: {e}")
        return None

# 3. AI විශ්ලේෂණය (Caching සමඟ)
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_text):
    model = load_model()
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_text}"
        2. Identify the exact source in the Tipitaka (Nikaya, Sutta, Verse).
        3. Provide a DEEP GRAMMATICAL ANALYSIS in a table format.
        4. List 3-5 relevant external article links or search queries for SuttaCentral, AccessToInsight, or WisdomLib.
        5. Explain the context (Nidana).
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "⚠️ දැනට මෙම Key එකේ සීමාව ඉක්මවා ඇත. කරුණාකර නැවත උත්සාහ කරන්න (Key Rotation ක්‍රියාත්මක වනු ඇත)."
            return f"විශ්ලේෂණයේදී දෝෂයක් සිදු විය: {str(e)}"
    return "AI පද්ධතිය ක්‍රියා විරහිතයි."

# 4. Header අංශය
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, ගැඹුරු ව්‍යාකරණ සහ මූලාශ්‍ර ගවේෂණය</p>", unsafe_allow_html=True)

# Tabs නිර්මාණය
tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

# --- Tab 1: පාලි සිට පරිවර්තනය ---
with tab1:
    if 'pali_text' not in st.session_state:
        st.session_state.pali_text = ""

    # පාලි විශේෂ අකුරු පුවරුව
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව (Pali Keyboard)"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("පාලි පාඨය මෙහි ඇතුළත් කරන්න:", value=st.session_state.pali_text, height=150, placeholder="උදා: නමෝ තස්ස භගවතෝ...")
    st.session_state.pali_text = pali_input

    if st.button("විශ්ලේෂණය කර මූලාශ්‍ර සොයන්න", type="primary", use_container_width=True):
        if pali_input.strip():
            with st.spinner('AI පද්ධතිය මගින් ගැඹුරු පර්යේෂණයක් සිදුකරමින් පවතී...'):
                result = get_pali_analysis(pali_input)
                st.markdown("### 📖 විශ්ලේෂණ වාර්තාව:")
                st.info(result)
                
                st.divider()
                st.markdown("#### 🔗 ක්ෂණික පර්යේෂණ සබැඳි (Quick Links):")
                c1, c2 = st.columns(2)
                with c1: st.link_button("📖 Tipitaka.lk (සෙවීම)", "https://tipitaka.lk/search", use_container_width=True)
                with c2: st.link_button("🌐 SuttaCentral (ගවේෂණය)", "https://suttacentral.net/", use_container_width=True)
        else:
            st.warning("⚠️ කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    eng_input = st.text_area("ඉංග්‍රීසි පාඨය මෙහි ඇතුළත් කරන්න (English to Pali):", height=150, placeholder="Enter English sentence to translate into Pali...")
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input.strip():
            model = load_model()
            if model:
                with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                    try:
                        res = model.generate_content(f"Translate this to Classical Pali with diacritics and grammar notes: {eng_input}")
                        st.success(res.text)
                    except Exception as e:
                        st.error(f"දෝෂයකි: {e}")

# --- Tab 3: මූලාශ්‍ර ---
with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ ශබ්දකෝෂ")
    st.markdown("""
    <div class="resource-link">🔹 <a href="https://tipitaka.lk/">Tipitaka.lk</a> - ත්‍රිපිටකය සිංහල අර්ථ සහිතව</div>
    <div class="resource-link">🔹 <a href="https://suttacentral.net/">SuttaCentral</a> - බහුභාෂා සූත්‍ර එකතුව</div>
    <div class="resource-link">🔹 <a href="https://www.wisdomlib.org/pali-dictionary">WisdomLib</a> - පාලි ශබ්දකෝෂය</div>
    <div class="resource-link">🔹 <a href="https://www.accesstoinsight.org/">Access to Insight</a> - ථේරවාද බෞද්ධ ලිපි</div>
    """, unsafe_allow_html=True)

st.markdown(f"<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
