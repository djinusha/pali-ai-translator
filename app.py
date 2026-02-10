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

# 2. API Keys කළමනාකරණය සහ Model එක තෝරා ගැනීම
def load_model():
    # Secrets තුළ ඇති Keys ලැයිස්තුවකට ගැනීම
    keys = []
    for i in range(1, 6):
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            keys.append(st.secrets[key_name])
    
    if not keys and "GEMINI_API_KEY" in st.secrets:
        keys.append(st.secrets["GEMINI_API_KEY"])

    if not keys:
        st.error("❌ API Keys කිසිවක් හමු නොවීය. කරුණාකර Secrets පරීක්ෂා කරන්න.")
        return None

    # අහඹු ලෙස Key එකක් තෝරාගෙන Configure කිරීම
    selected_key = random.choice(keys)
    
    try:
        genai.configure(api_key=selected_key)
        
        # 404 දෝෂය මඟහරවා ගැනීමට වඩාත් විශ්වාසදායක මාදිලි ලැයිස්තුව
        # 'models/' කොටස ඉවත් කර නම පමණක් භාවිතා කිරීමෙන් දෝෂය අවම වේ
        model_priority = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
        selected_model = None
        # පවතින මාදිලි පරීක්ෂා කිරීම
        for name in model_priority:
            try:
                # සෘජුවම මාදිලිය උත්සාහ කරන්න
                model = genai.GenerativeModel(name)
                return model
            except:
                continue
        return None
    except Exception as e:
        st.error(f"සම්බන්ධතාවයේ දෝෂයකි: {e}")
        return None

# 3. AI විශ්ලේෂණය සඳහා Caching ක්‍රමය
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    model = load_model() # සෑම වරකම Key එකක් Rotate කර ගනී
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
        2. Identify the exact source in the Tipitaka.
        3. Provide a DEEP GRAMMATICAL ANALYSIS (Padavigga) in a table.
        4. List 3-5 relevant references to SuttaCentral.net or Tipitaka.lk.
        5. Explain the context (Nidana).
        """
        try:
            # generate_content භාවිතයේදී version ස්වයංක්‍රීයව පාලනය වේ
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "⚠️ Quota සීමාව ඉක්මවා ඇත. කරුණාකර විනාඩියකින් උත්සාහ කරන්න."
            return f"AI පද්ධතියේ දෝෂයකි: {str(e)}"
    return "AI මාදිලිය සක්‍රීය කිරීමට නොහැකි විය."

# --- UI Header ---
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, ව්‍යාකරණ සහ මූලාශ්‍ර සහිත පූර්ණ පද්ධතිය</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

with tab1:
    if 'pali_text' not in st.session_state: st.session_state.pali_text = ""
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("Pali Text:", value=st.session_state.pali_text, height=150, placeholder="ගාථාවක් හෝ පාලි පාඨයක් මෙහි ඇතුළත් කරන්න...")
    st.session_state.pali_text = pali_input

    if st.button("විශ්ලේෂණය කර මූලාශ්‍ර සොයන්න", type="primary", use_container_width=True):
        if pali_input.strip():
            with st.spinner('AI පද්ධතිය මගින් ගැඹුරු පර්යේෂණයක් සිදුකරමින් පවතී...'):
                result = get_pali_analysis(pali_input)
                st.markdown("### 📖 ප්‍රතිඵලය:")
                st.info(result)
        else:
            st.warning("⚠️ කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")

with tab2:
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Type English here...")
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input.strip():
            model = load_model()
            if model:
                with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
                    try:
                        response = model.generate_content(f"Translate to Classical Pali: {eng_input}")
                        st.success(response.text)
                    except Exception as e:
                        st.error(f"දෝෂයකි: {e}")

with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ ශබ්දකෝෂ")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය සිංහල අර්ථ සහිතව</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර එකතුව</a></div>
    <div class="resource-link"><b>Access to Insight:</b> <a href="https://www.accesstoinsight.org/">ථේරවාද බෞද්ධ ලිපි</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
