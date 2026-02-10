import streamlit as st
import google.generativeai as genai
import random

# 1. පිටුවේ සැකසුම්
st.set_page_config(
    page_title="Pali AI Universal Scholar", 
    page_icon="☸️", 
    layout="wide"
)

# --- CSS Styling (Interface එක ලස්සන කිරීමට) ---
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

# 2. API Key Rotation පද්ධතිය
# සීමාවන් ඉක්මවා යාම වැළැක්වීමට Keys කිහිපයක් අතරින් එකක් තෝරා ගනී
def get_ai_model():
    # Secrets තුළ ඇති සියලුම Keys ලැයිස්තුවකට ගැනීම
    available_keys = []
    for i in range(1, 6):  # Key 1 සිට 5 දක්වා පරීක්ෂා කරයි
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            available_keys.append(st.secrets[key_name])
    
    # කිසිදු Key එකක් නැතිනම් සාමාන්‍ය Key එක බලයි
    if not available_keys and "GEMINI_API_KEY" in st.secrets:
        available_keys.append(st.secrets["GEMINI_API_KEY"])

    if not available_keys:
        st.error("❌ API Keys කිසිවක් හමු නොවීය. කරුණාකර Secrets පරීක්ෂා කරන්න.")
        return None

    try:
        # අහඹු ලෙස Key එකක් තෝරා ගැනීම (Traffic එක බෙදා හැරීමට)
        selected_key = random.choice(available_keys)
        genai.configure(api_key=selected_key)
        # වඩාත් ස්ථායී 1.5-flash මාදිලිය භාවිතා කිරීම
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"AI සම්බන්ධතාවයේ දෝෂයකි: {e}")
        return None

# 3. AI විශ්ලේෂණය සඳහා Caching ක්‍රමය
# එකම දේ නැවත සෙවීමේදී API එක වැය නොවේ
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    model = get_ai_model()
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
        2. Identify the exact source in the Tipitaka (Nikaya, Sutta, Verse).
        3. Provide a DEEP GRAMMATICAL ANALYSIS (Padavigga) in a table.
        4. List 3-5 relevant external article links or search queries for SuttaCentral, AccessToInsight, or WisdomLib related to this text.
        5. Explain the context (Nidana).
        """
        response = model.generate_content(prompt)
        return response.text
    return None

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, මූලාශ්‍ර සහ ශාස්ත්‍රීය ලිපි සබැඳි සහිත පද්ධතිය</p>", unsafe_allow_html=True)

# Tabs සැකසීම
tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

# --- Tab 1: පාලි සිට සිංහල/ඉංග්‍රීසි ---
with tab1:
    if 'pali_text' not in st.session_state:
        st.session_state.pali_text = ""

    # පාලි විශේෂ අකුරු පුවරුව
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("Pali Text:", value=st.session_state.pali_text, height=150, placeholder="ගාථාවක් හෝ පාලි පාඨයක් මෙහි ඇතුළත් කරන්න...")
    st.session_state.pali_text = pali_input

    if st.button("පරිවර්තනය සහ අදාළ ලිපි සොයන්න", type="primary", use_container_width=True):
        if not pali_input.strip():
            st.warning("⚠️ කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")
        else:
            with st.spinner('AI විශ්ලේෂණයක් සිදුකරමින් පවතී...'):
                try:
                    result = get_pali_analysis(pali_input)
                    if result:
                        st.markdown("### 📖 විශ්ලේෂණය සහ නිර්දේශිත ලිපි:")
                        st.info(result)
                        
                        st.divider()
                        st.markdown("#### 🔗 ක්ෂණික පර්යේෂණ සබැඳි (Quick Links):")
                        c1, c2 = st.columns(2)
                        with c1: st.link_button("📖 Tipitaka.lk (Search)", "https://tipitaka.lk/search", use_container_width=True)
                        with c2: st.link_button("🌐 SuttaCentral (Explore)", "https://suttacentral.net/", use_container_width=True)
                
                except Exception as e:
                    if "429" in str(e):
                        st.error("⚠️ සියලුම AI සීමාවන් ඉක්මවා ඇත. කරුණාකර විනාඩියකින් උත්සාහ කරන්න.")
                    else:
                        st.error(f"දෝෂයක් සිදු විය: {e}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Type English sentences to translate into Pali...")
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input.strip():
            with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                model = get_ai_model()
                if model:
                    try:
                        response = model.generate_content(f"Translate this to Classical Pali with grammar notes: {eng_input}")
                        st.success(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")

# --- Tab 3: බාහිර මූලාශ්‍ර සහ ලිපි ---
with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ වැදගත් මූලාශ්‍ර")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය (සිංහල අර්ථ සහිතව)</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර සහ විනය එකතුව</a></div>
    <div class="resource-link"><b>Access to Insight:</b> <a href="https://www.accesstoinsight.org/">ථේරවාද බෞද්ධ ලිපි සහ සූත්‍ර</a></div>
    <div class="resource-link"><b>WisdomLib:</b> <a href="https://www.wisdomlib.org/pali-dictionary">පාලි - ඉංග්‍රීසි ශබ්දකෝෂය</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
