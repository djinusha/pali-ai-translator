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
st.markdown("<p style='text-align: center;'>මූලාශ්‍ර සහ අතිරේක සම්පත් සහිත පූර්ණ පරිවර්තන පද්ධතිය</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

# --- Tab 1: පාලි සිට අනෙක් භාෂාවලට (ගැඹුරු ව්‍යාකරණ සහ මූලාශ්‍ර සමඟ) ---
with tab1:
    st.subheader("පාලි පාඨය, අර්ථය සහ ගැඹුරු ව්‍යාකරණ විවරණය")
    
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
        if pali_input and model:
            with st.spinner('දත්ත, මූලාශ්‍ර සහ ව්‍යාකරණ විශ්ලේෂණය කරමින් පවතී...'):
                # ගැඹුරු ව්‍යාකරණ සඳහා යාවත්කාලීන කළ Smart Prompt
                prompt = f"""
                As a world-class Pali Philologist and Tipitaka scholar:
                1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
                2. Identify the exact source in the Tipitaka (Nikaya, Sutta name, Vagga, or Dhammapada verse number).
                3. Provide 2-3 direct URLs or references to websites like SuttaCentral.net or Tipitaka.lk.
                4. Provide a DEEP GRAMMATICAL ANALYSIS (Padavigga) for each word in a table:
                   - Word
                   - Root (Dhatu)
                   - Grammatical Form (Noun Case/Vibhakti, Gender, Number OR Verb Tense, Person, Voice)
                   - English/Sinhala Meaning
                5. Explain any complex Sandhi (euphonic combination) or Samasa (compounds) present.
                6. Briefly explain the context (Nidana) and theological significance.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 📖 ගැඹුරු විශ්ලේෂණය සහ මූලාශ්‍ර:")
                    st.info(response.text)
                except Exception as e:
                    st.error(f"පරිවර්තනය අසාර්ථක විය: {e}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි (ව්‍යාකරණ මූලධර්ම සමඟ) ---
with tab2:
    st.subheader("English to Pali Translation & Grammar Guides")
    eng_input = st.text_area("Enter English text:", height=150, placeholder="පාලි භාෂාවට හැරවීමට අවශ්‍ය ඉංග්‍රීසි පාඨය මෙහි යොදන්න...")
    
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input and model:
            with st.spinner('පාලි භාෂාවට පරිවර්තනය වෙමින් පවතී...'):
                prompt = f"""
                1. Translate this English text to Classical Pali with correct diacritics: "{eng_input}"
                2. Provide a step-by-step grammatical explanation for the translation (Why these cases/verbs were chosen).
                3. Mention relevant rules from Pali grammar (like Kaccayana or Moggalana) if applicable.
                4. Recommend 1-2 Pali grammar books or online resources for further learning.
                """
                try:
                    response = model.generate_content(prompt)
                    st.success("#### Pali Translation & Deep Grammar Guide:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# Tab 3: ස්ථිර මූලාශ්‍ර (Resources)
with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ ශබ්දකෝෂ")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය සිංහල අර්ථ සහිතව</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර එකතුව (Pali, English, etc.)</a></div>
    <div class="resource-link"><b>Digital Pali Reader:</b> <a href="https://www.digitalpalireader.online/">පාලි ව්‍යාකරණ සහ පද විශ්ලේෂණය</a></div>
    <div class="resource-link"><b>WisdomLib:</b> <a href="https://www.wisdomlib.org/pali-dictionary">පාලි - ඉංග්‍රීසි ශබ්දකෝෂය</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
