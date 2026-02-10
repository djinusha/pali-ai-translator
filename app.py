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

# 2. API සහ Model එක පූරණය කිරීම (Caching භාවිතා කරමින්)
@st.cache_resource
def load_model():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # වඩාත් ස්ථායී 1.5 flash මාදිලිය භාවිතා කිරීම
            return genai.GenerativeModel('gemini-1.5-flash')
        except Exception:
            return None
    return None

model = load_model()

# 3. AI විශ්ලේෂණය සඳහා Caching ක්‍රමය
# මෙලෙස කිරීමෙන් එකම දේ නැවත සෙවීමේදී API Quota එක වැය නොවේ
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    prompt = f"""
    As a world-class Pali Philologist and Tipitaka scholar:
    1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
    2. Identify the exact source in the Tipitaka.
    3. Provide a DEEP GRAMMATICAL ANALYSIS in a table.
    4. Provide 3-5 relevant external article links or search queries for SuttaCentral, AccessToInsight, or WisdomLib.
    5. Explain the context (Nidana).
    """
    response = model.generate_content(prompt)
    return response.text

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
            st.error("API සම්බන්ධතාවයේ දෝෂයකි. කරුණාකර Secrets පරීක්ෂා කරන්න.")
        else:
            with st.spinner('ගැඹුරු විශ්ලේෂණයක් සිදුකරමින් පවතී...'):
                try:
                    # AI ප්‍රතිචාරය ලබා ගැනීම
                    result = get_pali_analysis(pali_input)
                    st.markdown("### 📖 විශ්ලේෂණය සහ නිර්දේශිත ලිපි:")
                    st.info(result)
                    
                    st.divider()
                    st.markdown("#### 🔗 ක්ෂණික පර්යේෂණ සබැඳි (Quick Research Links):")
                    row1_col1, row1_col2 = st.columns(2)
                    with row1_col1:
                        st.link_button("📖 Tipitaka.lk (Search Source)", "https://tipitaka.lk/search", use_container_width=True)
                    with row1_col2:
                        st.link_button("🌐 SuttaCentral (Explore)", "https://suttacentral.net/pitaka/sutta", use_container_width=True)
                
                # Quota සීමාව ඉක්මවා ගිය විට පෙන්වන පණිවිඩය
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        st.error("⚠️ අද දින සඳහා වෙන්කර ඇති AI සීමාව (Quota) අවසන් වී ඇත. කරුණාකර විනාඩියකින් පමණ නැවත උත්සාහ කරන්න.")
                        st.info("ඉඟිය: එකම දේ නැවත සෙවීමේදී මෙම දෝෂය ඇති නොවේ (Caching).")
                    else:
                        st.error(f"පරිවර්තනය අසාර්ථක විය: {e}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Type English here...")
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if not eng_input.strip():
            st.warning("⚠️ Please enter text to translate.")
        elif model:
            with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                try:
                    prompt = f"Translate this English text to Classical Pali with grammatical notes: {eng_input}"
                    response = model.generate_content(prompt)
                    st.success("#### Pali Translation:")
                    st.write(response.text)
                except Exception as e:
                    if "429" in str(e):
                        st.error("⚠️ සීමාව ඉක්මවා ඇත. කරුණාකර මඳ වේලාවකින් උත්සාහ කරන්න.")
                    else:
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
