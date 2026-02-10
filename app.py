import streamlit as st
import google.generativeai as genai

# 1. පිටුවේ සැකසුම්
st.set_page_config(
    page_title="Pali AI Scholar", 
    page_icon="☸️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf5; }
    .main-title { 
        color: #4a235a; 
        text-align: center; 
        font-size: 26px; 
        font-weight: bold; 
        padding: 10px;
        border-bottom: 2px solid #8e44ad;
        margin-bottom: 15px;
    }
    /* Keyboard බොත්තම් කුඩා සහ පිරිසිදු කිරීම */
    .pali-key {
        margin: 2px;
    }
    /* Footer සැකසුම */
    .footer { 
        position: relative;
        left: 0; bottom: 0; width: 100%; 
        background-color: #f1f1f1; 
        color: #4a235a; 
        text-align: center; 
        padding: 15px; 
        margin-top: 30px;
        border-top: 1px solid #ddd; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key missing!")

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Scholar</div>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 පාලි ➔ සිංහල", "🔡 English ➔ Pali", "📚 Resources"])

with tab1:
    # Session state for text
    if 'pali_text' not in st.session_state:
        st.session_state.pali_text = ""

    # --- අයිකනයක් සහිතව කීබෝඩ් එක සැඟවීම (Hidden Keyboard) ---
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව (Open Keyboard)"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()
        
        if st.button("❌ පිරිසිදු කරන්න (Clear Text)", use_container_width=True):
            st.session_state.pali_text = ""
            st.rerun()

    # Input area
    pali_input = st.text_area("පාලි පාඨය ඇතුළත් කරන්න:", value=st.session_state.pali_text, height=150, placeholder="මෙහි ටයිප් කරන්න...")
    
    # Update session state manually if user types
    st.session_state.pali_text = pali_input

    if st.button("පරිවර්තනය සහ මූලාශ්‍රය සොයන්න", type="primary", use_container_width=True):
        if pali_input:
            with st.spinner('විශ්ලේෂණය කරමින් පවතී...'):
                prompt = f"As a Pali expert, identify the source, provide Sinhala/English translations, and word meanings for: {pali_input}"
                try:
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("English to Pali")
    eng_input = st.text_area("Enter English text:", height=120)
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input:
            with st.spinner('Translating...'):
                prompt = f"Translate to Pali with diacritics: {eng_input}"
                response = model.generate_content(prompt)
                st.success(response.text)

with tab3:
    st.markdown("### 📚 අධ්‍යයන මූලාශ්‍ර")
    st.markdown("""
    * [Tipitaka.lk](https://tipitaka.lk/)
    * [SuttaCentral](https://suttacentral.net/)
    * [Pali Dictionary](https://www.wisdomlib.org/pali-dictionary)
    """)

# Footer
st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
