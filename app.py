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

# 2. API සහ Model එක තෝරා ගැනීම
def load_model():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            preferred_models = ['models/gemini-1.5-flash', 'models/gemini-pro', 'gemini-1.5-flash']
            selected_model = next((m for m in preferred_models if m in available_models), available_models[0])
            return genai.GenerativeModel(selected_model)
        except Exception as e:
            st.error(f"API සම්බන්ධතාවයේ දෝෂයකි: {e}")
            return None
    return None

model = load_model()

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
                2. Identify the exact source in the Tipitaka.
                3. Provide a DEEP GRAMMATICAL ANALYSIS in a table.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 📖 විශ්ලේෂණය:")
                    st.info(response.text)
                    
                    st.divider()
                    # සෘජු මූලාශ්‍ර සබැඳි එක් කිරීම
                    st.markdown("#### 🔗 මූලාශ්‍ර ගවේෂණය (Verified Links):")
                    l_col1, l_col2 = st.columns(2)
                    with l_col1:
                        st.link_button("📖 Tipitaka.lk මගින් සොයන්න", "https://tipitaka.lk/search", use_container_width=True)
                    with l_col2:
                        st.link_button("🌐 SuttaCentral මගින් කියවන්න", "https://suttacentral.net/pitaka/sutta", use_container_width=True)
                        
                except Exception as e:
                    st.error(f"පරිවර්තනය අසාර්ථක විය: {e}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Type English here...")
    
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if not eng_input.strip():
            st.warning("⚠️ Please enter text to translate.")
        elif model:
            with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                prompt = f"Translate this English text to Classical Pali with grammatical notes: {eng_input}"
                try:
                    response = model.generate_content(prompt)
                    st.success("#### Pali Translation:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# Tab 3: මූලාශ්‍ර
with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ ශබ්දකෝෂ")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය සිංහල අර්ථ සහිතව</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර එකතුව</a></div>
    <div class="resource-link"><b>WisdomLib:</b> <a href="https://www.wisdomlib.org/pali-dictionary">පාලි - ඉංග්‍රීසි ශබ්දකෝෂය</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
