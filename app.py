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
    .main-title { color: #4a235a; text-align: center; font-size: 30px; font-weight: bold; padding: 10px; border-bottom: 3px solid #8e44ad; }
    .sub-subtitle { text-align: center; color: #633971; font-size: 18px; margin-top: -10px; font-weight: 500; }
    .resource-link { background-color: #f4ecf7; padding: 10px; border-radius: 5px; border-left: 5px solid #8e44ad; margin: 5px 0px; }
    .footer { position: relative; text-align: center; padding: 20px; color: #7d3c98; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. වඩාත් ස්ථායී AI මාදිලිය තෝරා ගැනීමේ ක්‍රියාවලිය (404 Error එක මඟහරවා ගැනීමට)
def get_ai_model():
    available_keys = []
    for i in range(1, 6):
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            available_keys.append(st.secrets[key_name])
    
    if not available_keys and "GEMINI_API_KEY" in st.secrets:
        available_keys.append(st.secrets["GEMINI_API_KEY"])

    if not available_keys:
        st.error("❌ API Keys කිසිවක් හමු නොවීය.")
        return None

    try:
        selected_key = random.choice(available_keys)
        genai.configure(api_key=selected_key)
        
        # 404 දෝෂය වැළැක්වීමට වඩාත් විශ්වාසදායක මාදිලි නාමයන් මෙලෙස භාවිතා කළ හැක
        # පළමුව gemini-1.5-flash උත්සාහ කරයි, එය නැත්නම් gemini-pro උත්සාහ කරයි
        for model_name in ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-pro']:
            try:
                model = genai.GenerativeModel(model_name)
                # මාදිලිය වැඩ කරන්නේදැයි පරීක්ෂා කිරීමට කුඩා පරීක්ෂණයක් (optional)
                return model
            except:
                continue
        return None
    except Exception as e:
        st.error(f"සම්බන්ධතාවයේ ගැටලුවකි: {e}")
        return None

# 3. AI විශ්ලේෂණය සඳහා Caching ක්‍රමය
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    model = get_ai_model()
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
        2. Identify the exact source in the Tipitaka.
        3. Provide a DEEP GRAMMATICAL ANALYSIS in a table.
        4. List 3-5 relevant external article links or search terms for SuttaCentral, AccessToInsight, or WisdomLib.
        5. Explain the context (Nidana).
        """
        response = model.generate_content(prompt)
        return response.text
    return "AI මාදිලිය පූරණය කිරීමට නොහැකි විය."

# --- UI Header ---
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, මූලාශ්‍ර සහ ශාස්ත්‍රීය ලිපි සබැඳි සහිත පද්ධතිය</p>", unsafe_allow_html=True)

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

    if st.button("පරිවර්තනය සහ අදාළ ලිපි සොයන්න", type="primary", use_container_width=True):
        if not pali_input.strip():
            st.warning("⚠️ කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")
        else:
            with st.spinner('ගැඹුරු විශ්ලේෂණයක් සිදුකරමින් පවතී...'):
                try:
                    result = get_pali_analysis(pali_input)
                    st.markdown("### 📖 විශ්ලේෂණය:")
                    st.info(result)
                    st.divider()
                    st.markdown("#### 🔗 ක්ෂණික පර්යේෂණ සබැඳි:")
                    c1, c2 = st.columns(2)
                    with c1: st.link_button("📖 Tipitaka.lk", "https://tipitaka.lk/search", use_container_width=True)
                    with c2: st.link_button("🌐 SuttaCentral", "https://suttacentral.net/", use_container_width=True)
                except Exception as e:
                    st.error(f"දෝෂයක් සිදු විය: {e}")

with tab2:
    eng_input = st.text_area("Enter English text:", height=150)
    if st.button("Translate to Pali", type="primary"):
        if eng_input.strip():
            with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                model = get_ai_model()
                if model:
                    response = model.generate_content(f"Translate to Classical Pali: {eng_input}")
                    st.success(response.text)

with tab3:
    st.markdown("### 📚 මූලාශ්‍ර")
    st.markdown("""
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර එකතුව</a></div>
    <div class="resource-link"><b>Access to Insight:</b> <a href="https://www.accesstoinsight.org/">ථේරවාද බෞද්ධ ලිපි</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
