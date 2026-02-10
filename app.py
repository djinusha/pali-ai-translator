import streamlit as st
import google.generativeai as genai

# 1. පිටුවේ සැකසුම්
st.set_page_config(
    page_title="Pali AI Universal Scholar", 
    page_icon="☸️", 
    layout="wide"
)

# --- CSS මගින් මුහුණත හැඩගැන්වීම ---
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

# 2. API Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key missing in Secrets!")

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Pali-Sinhala-English භාෂා ත්‍රිත්වයෙන්ම ක්‍රියාත්මක වන පද්ධතිය</p>", unsafe_allow_html=True)

# Tabs - මෙන්න මෙතැනින් තමයි ඔබ ඉල්ලූ පරිදි කොටස් වෙන් වෙන්නේ
tab1, tab2, tab3 = st.tabs(["🔄 Pali to Sinhala & English", "🔡 English to Pali", "📚 Resources"])

# --- Tab 1: පාලි සිට සිංහල සහ ඉංග්‍රීසි ---
with tab1:
    st.subheader("පාලි පාඨයක් සිංහලට සහ ඉංග්‍රීසියට පරිවර්තනය")
    
    if 'pali_text' not in st.session_state:
        st.session_state.pali_text = ""

    # සැඟවිය හැකි කීබෝඩ් එක
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව (Open Keyboard)"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("Pali Text:", value=st.session_state.pali_text, height=150, placeholder="පාලි වාක්‍යය හෝ ගාථාව මෙහි ඇතුළත් කරන්න...")
    st.session_state.pali_text = pali_input

    if st.button("පරිවර්තනය කරන්න (Translate)", type="primary", use_container_width=True):
        if pali_input:
            with st.spinner('විශ්ලේෂණය කරමින් පවතී...'):
                # AI එකට දෙන උපදෙස් වලට සිංහල සහ ඉංග්‍රීසි යන දෙකම ඇතුළත් කළා
                prompt = f"""
                As a Pali scholar:
                1. Translate this text into BOTH Sinhala and English: {pali_input}
                2. Identify the source (Nikaya/Sutta/Gatha source).
                3. Provide word-by-word meanings in a table.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 📖 ප්‍රතිඵලය (Result):")
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    st.subheader("ඉංග්‍රීසි පාඨයක් පාලි භාෂාවට (English to Pali)")
    eng_input = st.text_area("Enter English text or phrase:", height=150, placeholder="Type English here to get Pali translation...")
    
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input:
            with st.spinner('Translating to Pali...'):
                prompt = f"Translate this English text into classical Pali with correct diacritics (ā, ī, ṃ, etc.): {eng_input}. Explain the choice of Pali words."
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
    * [Tipitaka.lk](https://tipitaka.lk/) - පාලි ත්‍රිපිටකය සිංහල අර්ථ සහිතව.
    * [SuttaCentral](https://suttacentral.net/) - පාලි සූත්‍ර ඉංග්‍රීසි ඇතුළු භාෂා ගණනාවකින්.
    * [WisdomLib](https://www.wisdomlib.org/pali-dictionary) - පාලි-ඉංග්‍රීසි ශබ්දකෝෂය.
    """)

# Footer
st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
