import streamlit as st
import google.generativeai as genai

# 1. පිටුවේ සැකසුම්
st.set_page_config(
    page_title="Pali AI Universal Scholar", 
    page_icon="☸️", 
    layout="wide"
)

# --- CSS Styling (පෙනුම අලංකාර කිරීමට) ---
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

# 2. AI මාදිලිය තෝරා ගැනීමේ ක්‍රියාවලිය (Fallback පද්ධතියක් සහිතව)
def load_model():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # පවතින මාදිලි ලැයිස්තුව ලබා ගැනීම
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # වඩාත් සුදුසු මාදිලි පෙළගස්වන අනුපිළිවෙල
            # 1.5 flash සාමාන්‍යයෙන් වේගවත් සහ ධාරිතාව වැඩියි
            priority_list = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
            
            selected = None
            for p_model in priority_list:
                if p_model in models:
                    selected = p_model
                    break
            
            if not selected:
                selected = models[0] # කිසිවක් නොමැති නම් පවතින පළමු එක ගන්න
                
            return genai.GenerativeModel(selected)
        except Exception as e:
            st.error(f"API සම්බන්ධතාවයේ ගැටලුවකි: {e}")
            return None
    return None

model = load_model()

# 3. AI විශ්ලේෂණය සඳහා Caching ක්‍රමය (Quota ඉතිරි කර ගැනීමට)
@st.cache_data(show_spinner=False)
def get_pali_analysis(pali_input):
    if model:
        prompt = f"""
        As a world-class Pali Philologist and Tipitaka scholar:
        1. Translate this Pali text into BOTH Sinhala and English: "{pali_input}"
        2. Identify the exact source in the Tipitaka.
        3. Provide a DEEP GRAMMATICAL ANALYSIS in a table.
        4. List 3-5 relevant external article links or search queries for SuttaCentral, AccessToInsight, or WisdomLib.
        5. Explain the context (Nidana).
        """
        response = model.generate_content(prompt)
        return response.text
    return None

# 4. Header
st.markdown("<div class='main-title'>☸️ Pali AI Universal Scholar</div>", unsafe_allow_html=True)
st.markdown("<p class='sub-subtitle'>පරිවර්තනය, මූලාශ්‍ර සහ ශාස්ත්‍රීය ලිපි සබැඳි සහිත පූර්ණ පද්ධතිය</p>", unsafe_allow_html=True)

# Tabs සැකසීම
tab1, tab2, tab3 = st.tabs(["🔄 පාලි ➔ සිංහල/English", "🔡 English ➔ පාලි", "📚 බාහිර මූලාශ්‍ර"])

# --- Tab 1: පාලි සිට අනෙක් භාෂාවලට ---
with tab1:
    if 'pali_text' not in st.session_state:
        st.session_state.pali_text = ""

    # විශේෂ පාලි අකුරු පුවරුව
    with st.expander("⌨️ පාලි විශේෂ අකුරු පුවරුව"):
        char_list = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ', 'ṇḍ']
        cols = st.columns(6)
        for i, char in enumerate(char_list):
            if cols[i % 6].button(char, key=f"kb_{char}", use_container_width=True):
                st.session_state.pali_text += char
                st.rerun()

    pali_input = st.text_area("Pali Text:", value=st.session_state.pali_text, height=150, placeholder="පාලි පාඨය මෙහි ඇතුළත් කරන්න...")
    st.session_state.pali_text = pali_input

    if st.button("පරිවර්තනය සහ අදාළ ලිපි සොයන්න", type="primary", use_container_width=True):
        if not pali_input.strip():
            st.warning("⚠️ කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")
        elif not model:
            st.error("AI මාදිලිය පූරණය වී නැත. කරුණාකර Secrets පරීක්ෂා කරන්න.")
        else:
            with st.spinner('AI විශ්ලේෂණයක් සිදුකරමින් පවතී...'):
                try:
                    result = get_pali_analysis(pali_input)
                    st.markdown("### 📖 විශ්ලේෂණය සහ නිර්දේශිත ලිපි:")
                    st.info(result)
                    
                    st.divider()
                    st.markdown("#### 🔗 ක්ෂණික පර්යේෂණ සබැඳි (Verified Sources):")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.link_button("📖 Tipitaka.lk (Search)", "https://tipitaka.lk/search", use_container_width=True)
                    with c2:
                        st.link_button("🌐 SuttaCentral (Explore)", "https://suttacentral.net/", use_container_width=True)
                
                except Exception as e:
                    if "429" in str(e):
                        st.error("⚠️ දිනකට හිමි නොමිලේ ලබාදෙන සීමාව (Quota) ඉක්මවා ඇත. කරුණාකර මඳ වේලාවකින් නැවත උත්සාහ කරන්න.")
                    elif "404" in str(e):
                        st.error("⚠️ තෝරාගත් AI මාදිලිය හමු නොවුණි. වෙනත් මාදිලියක් උත්සාහ කරමින් පවතී...")
                        st.rerun()
                    else:
                        st.error(f"තාක්ෂණික දෝෂයක් සිදු විය: {e}")

# --- Tab 2: ඉංග්‍රීසි සිට පාලි ---
with tab2:
    eng_input = st.text_area("Enter English text:", height=150, placeholder="Translate English into Pali...")
    if st.button("Translate to Pali", type="primary", use_container_width=True):
        if eng_input.strip() and model:
            with st.spinner('Translating...'):
                try:
                    prompt = f"Translate to Classical Pali with grammatical breakdown: {eng_input}"
                    response = model.generate_content(prompt)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Tab 3: බාහිර මූලාශ්‍ර ---
with tab3:
    st.markdown("### 📚 පාලි ධර්ම ග්‍රන්ථ සහ ශාස්ත්‍රීය මූලාශ්‍ර")
    st.markdown("""
    <div class="resource-link"><b>Tipitaka.lk:</b> <a href="https://tipitaka.lk/">ත්‍රිපිටකය (සිංහල අර්ථ සහිතව)</a></div>
    <div class="resource-link"><b>SuttaCentral:</b> <a href="https://suttacentral.net/">බහුභාෂා සූත්‍ර සහ විනය එකතුව</a></div>
    <div class="resource-link"><b>Access to Insight:</b> <a href="https://www.accesstoinsight.org/">ථේරවාද බෞද්ධ ලිපි සහ සූත්‍ර</a></div>
    <div class="resource-link"><b>Digital Pali Reader:</b> <a href="https://www.digitalpalireader.online/">පාලි පද විශ්ලේෂක මෙවලම</a></div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Created by Jinusha Dissanayaka | Powered by Gemini AI</div>", unsafe_allow_html=True)
