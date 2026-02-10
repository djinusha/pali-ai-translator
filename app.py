import streamlit as st
import google.generativeai as genai

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

# 2. API සහ Model එක පූරණය කිරීම (දෝෂ රහිතව)
@st.cache_resource
def load_model():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # 'gemini-1.5-flash' යනු දැනට වඩාත් ස්ථාවර සහ වේගවත් මාදිලියයි
            # මෙහිදී 'models/' කොටස ඉවත් කර සරලව නම පමණක් භාවිතා කිරීමෙන් 404 දෝෂය අවම වේ
            return genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            return None
    return None

model = load_model()

# 3. AI විශ්ලේෂණය සඳහා Caching ක්‍රමය (API Quota ඉතිරි කර ගැනීමට)
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
        2. Identify the exact source in the Tipitaka.
        3. Provide a DEEP GRAMMATICAL ANALYSIS (Padavigga) in a table.
        4. List 3-5 relevant external article links or search terms for sites like SuttaCentral, AccessToInsight, or WisdomLib specifically related to this text.
        5. Explain the context (Nidana).
        """
        response = model.generate_content(prompt)
        return response.text
    return None

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, මූලාශ්‍ර සහ ශාස්ත්‍රීය ලිපි සබැඳි සහිත පූර්ණ පද්ධතිය</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

# --- Tab 1: පාලි සිට අනෙක් භාෂාවලට ---
with tab1:
    if 'pali_text' not in st.session_state:
        st.session_state.pali_text = ""

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
        elif not model:
            st.error("❌ AI සම්බන්ධතාවය අසාර්ථකයි. කරුණාකර API Key එක පරීක්ෂා කරන්න.")
        else:
            with st.spinner('AI මගින් ගැඹුරු විශ්ලේෂණයක් සිදුකරමින් පවතී...'):
                try:
                    result = get_pali_analysis(pali_input)
                    if result:
                        st.markdown("### 📖 විශ්ලේෂණය සහ නිර්දේශිත ලිපි:")
                        st.info(result)
                        
                        st.divider()
                        st.markdown("#### 🔗 ක්ෂණික පර්යේෂණ සබැඳි (Quick Research Links):")
                        c1, c2 = st.columns(2)
                        with c1: st.link_button("📖 Tipitaka.lk (Search Source)", "https://tipitaka.lk/search", use_container_width=True)
                        with c2: st.link_button("🌐 SuttaCentral (Explore)", "https://suttacentral.net/", use_container_width=True)
                    else:
                        st.error("ප්‍රතිචාරයක් ලබා ගැනීමට නොහැකි විය.")
                
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg:
                        st.error("⚠️ AI සීමාව (Quota) ඉක්මවා ඇත. කරුණාකර විනාඩියකින් නැවත උත්සාහ කරන්න.")
                    elif "404" in error_msg or "not found" in error_msg.lower():
                        st.error("⚠️ භාවිතා කරන AI මාදිලිය තාවකාලිකව අක්‍රියයි. කරුණාකර මඳ වේලාවකින් නැවත උත්සාහ කරන්න.")
                    else:
                        st.error(f"දෝෂයක් සිදු විය: {error_msg}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Type English here...")
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if not eng_input.strip():
            st.warning("⚠️ Please enter text.")
        elif model:
            with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                try:
                    prompt = f"Translate to Classical Pali with grammatical notes: {eng_input}"
                    response = model.generate_content(prompt)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Tab 3: මූලාශ්‍ර ---
with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ වැදගත් ලිපි මූලාශ්‍ර")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය සිංහල අර්ථ සහිතව</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර සහ පරිවර්තන එකතුව</a></div>
    <div class="resource-link"><b>Access to Insight:</b> <a href="https://www.accesstoinsight.org/">ථේරවාද බෞද්ධ ලිපි සහ සූත්‍ර</a></div>
    <div class="resource-link"><b>WisdomLib:</b> <a href="https://www.wisdomlib.org/pali-dictionary">පාලි - ඉංග්‍රීසි ශබ්දකෝෂය</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
