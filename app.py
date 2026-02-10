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
    .footer { 
        position: relative;
        text-align: center; 
        padding: 20px; 
        color: #7d3c98;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API සහ Model එක තෝරා ගැනීම (Error Handling සමඟ)
def load_model():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # පද්ධතියේ ඇති වැඩ කරන මාදිලියක් ස්වයංක්‍රීයව තෝරා ගැනීම
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # වැඩි කැමැත්තක් දක්වන මාදිලි පෙළ (ප්‍රමුඛතාවය අනුව)
            preferred_models = ['models/gemini-1.5-flash', 'models/gemini-pro', 'gemini-1.5-flash']
            
            selected_model = None
            for model_name in preferred_models:
                if model_name in available_models:
                    selected_model = model_name
                    break
            
            if not selected_model:
                selected_model = available_models[0]
                
            return genai.GenerativeModel(selected_model)
        except Exception as e:
            st.error(f"API සම්බන්ධතාවයේ දෝෂයකි: {e}")
            return None
    else:
        st.error("Secrets හි API Key එක හමු නොවීය.")
        return None

model = load_model()

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>සිංහල, ඉංග්‍රීසි සහ පාලි භාෂා ත්‍රිත්වයෙන්ම ක්‍රියාත්මක වේ</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල සහ ඉංග්‍රීසි", "🔡 ඉංග්‍රීසි ➔ පාලි", "📚 මූලාශ්‍ර"])

# --- Tab 1: පාලි සිට අනෙක් භාෂාවලට ---
with tab1:
    st.subheader("පාලි පාඨයක් සිංහලට සහ ඉංග්‍රීසියට පරිවර්තනය")
    
    if 'pali_text' not in st.session_state:
        st.session_state.pali_text = ""

    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව (Open Keyboard)"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("Pali Text:", value=st.session_state.pali_text, height=150, placeholder="පාලි වාක්‍යය හෝ ගාථාව මෙහි ඇතුළත් කරන්න...")
    st.session_state.pali_text = pali_input

    if st.button("පරිවර්තනය කරන්න", type="primary", use_container_width=True):
        if pali_input and model:
            with st.spinner('විශ්ලේෂණය කරමින් පවතී...'):
                prompt = f"""
                As a Pali scholar:
                1. Translate this text into BOTH Sinhala and English: {pali_input}
                2. Identify the source (Nikaya/Sutta/Gatha source).
                3. Provide word-by-word meanings in a table.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 📖 ප්‍රතිඵලය:")
                    st.info(response.text)
                except Exception as e:
                    st.error(f"පරිවර්තනය අසාර්ථක විය: {e}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    st.subheader("ඉංග්‍රීසි පාඨයක් පාලි භාෂාවට (English to Pali)")
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Type English here...")
    
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input and model:
            with st.spinner('Translating to Pali...'):
                prompt = f"Translate this English text into classical Pali with correct diacritics: {eng_input}"
                try:
                    response = model.generate_content(prompt)
                    st.success("#### Pali Translation:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# Tab 3: Resources
with tab3:
    st.markdown("### 📚 අධ්‍යයන මූලාශ්‍ර")
    st.markdown("""
    * [Tipitaka.lk](https://tipitaka.lk/)
    * [SuttaCentral](https://suttacentral.net/)
    * [WisdomLib Pali Dictionary](https://www.wisdomlib.org/pali-dictionary)
    """)

# Footer
st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
