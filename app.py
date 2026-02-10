import streamlit as st
import google.generativeai as genai
import random

# 1. පිටුවේ සැකසුම්
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

# 2. API Keys කිහිපයක් කළමනාකරණය කරන පද්ධතිය (Key Rotation)
def load_model():
    # Secrets තුළ ඇති සියලුම Keys ලැයිස්තුවකට ගැනීම
    available_keys = []
    for i in range(1, 6): # Key 1 සිට 5 දක්වා පරීක්ෂා කරයි
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            available_keys.append(st.secrets[key_name])
    
    # කිසිදු අංකනය කළ Key එකක් නැතිනම් සාමාන්‍ය එක බලයි
    if not available_keys and "GEMINI_API_KEY" in st.secrets:
        available_keys.append(st.secrets["GEMINI_API_KEY"])

    if not available_keys:
        st.error("❌ API Keys කිසිවක් හමු නොවීය. කරුණාකර Secrets පරීක්ෂා කරන්න.")
        return None

    try:
        # අහඹු ලෙස Key එකක් තෝරා ගැනීම
        selected_key = random.choice(available_keys)
        genai.configure(api_key=selected_key)
        
        # 404 දෝෂය මඟහරවා ගැනීමට වඩාත් ස්ථාවර මාදිලි නාමයන් පරීක්ෂා කිරීම
        # flash සහ pro මාදිලි දෙකම fallback ලෙස ඇතුළත් කර ඇත
        for model_name in ['gemini-1.5-flash', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(model_name)
                return model
            except:
                continue
        return None
    except Exception as e:
        st.error(f"API සම්බන්ධතාවයේ දෝෂයකි: {e}")
        return None

model = load_model()

# 3. AI විශ්ලේෂණය සඳහා Caching (Quota ඉතිරි කිරීමට)
@st.cache_data(show_spinner=False)
def get_analysis_response(prompt_text):
    if model:
        try:
            response = model.generate_content(prompt_text)
            return response.text
        except Exception as e:
            return f"Error: {e}"
    return "Model not initialized."

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>මූලාශ්‍ර සහ අතිරේක සම්පත් සහිත පූර්ණ පරිවර්තන පද්ධතිය</p>", unsafe_allow_html=True)

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

    if st.button("පරිවර්තනය සහ මූලාශ්‍ර සොයන්න", type="primary", use_container_width=True):
        if not pali_input.strip():
            st.warning("⚠️ කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")
        elif model:
            with st.spinner('විශ්ලේෂණය කරමින් පවතී...'):
                prompt = f"""
                As a world-class Pali Philologist and Tipitaka scholar:
                1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
                2. Identify the exact source in the Tipitaka (Nikaya, Sutta name, Vagga, or Dhammapada verse number).
                3. Provide direct references to SuttaCentral.net or Tipitaka.lk.
                4. Provide a DEEP GRAMMATICAL ANALYSIS (Padavigga) in a table including Root, Case/Tense, Gender, and Number.
                5. Explain complex Sandhi or Samasa.
                6. Explain the context (Nidana).
                """
                result = get_analysis_response(prompt)
                st.markdown("### 📖 විශ්ලේෂණය:")
                st.info(result)

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Type English here...")
    
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input.strip() and model:
            with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                prompt = f"""
                1. Translate this English text to Classical Pali with correct diacritics: "{eng_input}"
                2. Provide a step-by-step grammatical explanation.
                3. Mention relevant rules from Pali grammar (Kaccayana/Moggalana).
                """
                result = get_analysis_response(prompt)
                st.success("#### Pali Translation & Deep Grammar Guide:")
                st.write(result)

# Tab 3: මූලාශ්‍ර
with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ ශබ්දකෝෂ")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය සිංහල අර්ථ සහිතව</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර එකතුව</a></div>
    <div class="resource-link"><b>Digital Pali Reader:</b> <a href="https://www.digitalpalireader.online/">පද විශ්ලේෂණය</a></div>
    <div class="resource-link"><b>WisdomLib:</b> <a href="https://www.wisdomlib.org/pali-dictionary">පාලි - ඉංග්‍රීසි ශබ්දකෝෂය</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
