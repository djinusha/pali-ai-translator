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

# 2. API සහ Model එක පූරණය කිරීම (404 Error එක මඟහරවා ගැනීම සඳහා)
@st.cache_resource
def load_model():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # 'gemini-pro' මාදිලිය සාමාන්‍යයෙන් වඩාත් ස්ථාවරව 404 දෝෂ රහිතව ක්‍රියා කරයි
            return genai.GenerativeModel('gemini-pro')
        except Exception as e:
            st.error(f"සම්බන්ධතාවයේ ගැටලුවකි: {e}")
            return None
    return None

model = load_model()

# 3. AI විශ්ලේෂණය සඳහා Caching ක්‍රමය
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
        2. Identify the exact source in the Tipitaka.
        3. Provide a DEEP GRAMMATICAL ANALYSIS in a table.
        4. List 3-5 relevant external article links or search queries (e.g., from SuttaCentral or AccessToInsight) related to this text.
        5. Explain the context (Nidana).
        """
        response = model.generate_content(prompt)
        return response.text
    return "Model not initialized."

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, මූලාශ්‍ර සහ ශාස්ත්‍රීය ලිපි සබැඳි සහිත පද්ධතිය</p>", unsafe_allow_html=True)

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
            st.error("AI මාදිලිය පූරණය කිරීමට නොහැකි විය. කරුණාකර ඔබගේ API Key එක පරීක්ෂා කරන්න.")
        else:
            with st.spinner('ගැඹුරු විශ්ලේෂණයක් සිදුකරමින් පවතී...'):
                try:
                    result = get_pali_analysis(pali_input)
                    st.markdown("### 📖 විශ්ලේෂණය සහ නිර්දේශිත ලිපි:")
                    st.info(result)
                    
                    st.divider()
                    st.markdown("#### 🔗 ක්ෂණික පර්යේෂණ සබැඳි (Quick Links):")
                    c1, c2 = st.columns(2)
                    with c1: st.link_button("📖 Tipitaka.lk (Search)", "https://tipitaka.lk/search", use_container_width=True)
                    with c2: st.link_button("🌐 SuttaCentral (Explore)", "https://suttacentral.net/", use_container_width=True)
                
                except Exception as e:
                    if "429" in str(e):
                        st.error("⚠️ AI සීමාව (Quota) ඉක්මවා ඇත. කරුණාකර විනාඩියකින් උත්සාහ කරන්න.")
                    elif "404" in str(e):
                        st.error("⚠️ තෝරාගත් AI මාදිලිය දැනට අක්‍රියයි. කරුණාකර මඳ වේලාවකින් නැවත උත්සාහ කරන්න.")
                    else:
                        st.error(f"දෝෂයක් සිදු විය: {e}")

# (Tab 2 සහ Tab 3 පෙර පරිදිම පවතී)
with tab2:
    eng_input = st.text_area("Enter English text:", height=150)
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input.strip() and model:
            with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                try:
                    prompt = f"Translate to Classical Pali with grammatical notes: {eng_input}"
                    response = model.generate_content(prompt)
                    st.success(response.text)
                except Exception as e: st.error(f"Error: {e}")

with tab3:
    st.markdown("### 📚 වැදගත් ලිපි සහ මූලාශ්‍ර")
    st.markdown("""
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර එකතුව</a></div>
    <div class="resource-link"><b>Access to Insight:</b> <a href="https://www.accesstoinsight.org/">ථේරවාද බෞද්ධ මූලාශ්‍ර</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
