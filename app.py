import streamlit as st
import google.generativeai as genai
import random

# 1. පිටුවේ සැකසුම් (Page Configuration)
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

# 2. වඩාත් ස්ථායී AI මාදිලිය සහ API Key එක තෝරා ගැනීම
def get_working_model():
    # Secrets තුළ ඇති සියලුම API Keys ලැයිස්තුවකට ගැනීම
    keys = []
    for i in range(1, 6):
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            keys.append(st.secrets[key_name])
    
    if not keys and "GEMINI_API_KEY" in st.secrets:
        keys.append(st.secrets["GEMINI_API_KEY"])

    if not keys:
        return None, "API Keys කිසිවක් හමු නොවීය. කරුණාකර Secrets පරීක්ෂා කරන්න."

    # පවතින Keys අතරින් එකක් අහඹු ලෙස තෝරා ගැනීම (Rotation)
    selected_key = random.choice(keys)
    
    try:
        genai.configure(api_key=selected_key)
        
        # 404 දෝෂය මඟහරවා ගැනීමට පවතින මාදිලි අනුපිළිවෙලින් පරීක්ෂා කිරීම
        for model_name in ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-pro']:
            try:
                model = genai.GenerativeModel(model_name)
                return model, None
            except:
                continue
        return None, "සුදුසු AI මාදිලියක් සොයාගත නොහැකි විය."
    except Exception as e:
        return None, str(e)

# 3. AI විශ්ලේෂණය (Caching සමඟ Quota ඉතිරි කිරීමට)
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    model, error = get_working_model()
    if error:
        return f"දෝෂයකි: {error}"
    
    prompt = f"""
    As a world-class Pali Philologist and Tipitaka scholar:
    1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
    2. Identify the exact source in the Tipitaka (Nikaya, Sutta, Verse).
    3. Provide a DEEP GRAMMATICAL ANALYSIS in a table format.
    4. List 3-5 relevant external article links or search terms for SuttaCentral, AccessToInsight, or WisdomLib related to this text.
    5. Explain the context (Nidana).
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "⚠️ Quota සීමාව ඉක්මවා ඇත. කරුණාකර විනාඩියකින් උත්සාහ කරන්න."
        return f"විශ්ලේෂණය අසාර්ථක විය: {str(e)}"

# 4. Header කොටස
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, මූලාශ්‍ර සහ ශාස්ත්‍රීය ලිපි සබැඳි සහිත පූර්ණ පද්ධතිය</p>", unsafe_allow_html=True)

# Tabs සැකසීම
tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

# --- Tab 1: පාලි සිට සිංහල/ඉංග්‍රීසි ---
with tab1:
    if 'pali_text' not in st.session_state:
        st.session_state.pali_text = ""

    # විශේෂ අකුරු පුවරුව
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව (Pali Keyboard)"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("Pali Text:", value=st.session_state.pali_text, height=150, placeholder="ගාථාවක් හෝ පාලි පාඨයක් මෙහි ඇතුළත් කරන්න...")
    st.session_state.pali_text = pali_input

    if st.button("විශ්ලේෂණය කර ලිපි සොයන්න", type="primary", use_container_width=True):
        if not pali_input.strip():
            st.warning("⚠️ කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")
        else:
            with st.spinner('AI මගින් ගැඹුරු පර්යේෂණයක් සිදුකරමින් පවතී...'):
                result = get_pali_analysis(pali_input)
                st.markdown("### 📖 විශ්ලේෂණය සහ නිර්දේශිත ලිපි:")
                st.info(result)
                
                st.divider()
                st.markdown("#### 🔗 ක්ෂණික පර්යේෂණ සබැඳි (Quick Links):")
                c1, c2 = st.columns(2)
                with c1: st.link_button("📖 Tipitaka.lk (Search)", "https://tipitaka.lk/search", use_container_width=True)
                with c2: st.link_button("🌐 SuttaCentral (Explore)", "https://suttacentral.net/", use_container_width=True)

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Type English here to translate into Pali...")
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input.strip():
            with st.spinner('Translating...'):
                model, error = get_working_model()
                if model:
                    try:
                        response = model.generate_content(f"Translate this to Classical Pali with grammar notes: {eng_input}")
                        st.success(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error(error)

# --- Tab 3: බාහිර මූලාශ්‍ර ---
with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ වැදගත් මූලාශ්‍ර")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය (සිංහල අර්ථ සහිතව)</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර සහ විනය එකතුව</a></div>
    <div class="resource-link"><b>Access to Insight:</b> <a href="https://www.accesstoinsight.org/">ථේරවාද බෞද්ධ ලිපි සහ සූත්‍ර</a></div>
    <div class="resource-link"><b>WisdomLib:</b> <a href="https://www.wisdomlib.org/pali-dictionary">පාලි - ඉංග්‍රීසි ශබ්දකෝෂය</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
