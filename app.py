import streamlit as st
import google.generativeai as genai

# 1. පිටුවේ සැකසුම් (Page Configuration)
st.set_page_config(
    page_title="AI පාලි පරිවර්තකය", 
    page_icon="☸️",
    layout="centered"
)

# 2. වැඩ කරන මාදිලියක් (Model) සොයා ගැනීමේ ශ්‍රිතය
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']:
            if preferred in available_models:
                return preferred
        return available_models[0] if available_models else None
    except:
        return None

# 3. API සම්බන්ධතාවය (API Connection)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model_id = get_working_model()
    if model_id:
        model = genai.GenerativeModel(model_id)
    else:
        st.error("මාදිලියක් සොයාගත නොහැක.")
else:
    st.error("Secrets හි API Key එක හමු නොවීය.")

# 4. පරිශීලක මුහුණත (User Interface)
st.title("☸️ AI පාලි පරිවර්තකය")
st.write("පාලි පාඨ සිංහල සහ ඉංග්‍රීසි භාෂාවට පරිවර්තනය කරන්න.")
st.markdown("---")

# --- පාලි විශේෂ අකුරු පුවරුව (Virtual Keyboard) ---
st.write("විශේෂ අකුරු අවශ්‍ය නම් මෙතැනින් තෝරන්න:")

# Session State මගින් ටයිප් කරන දේ මතක තබා ගැනීම
if 'pali_input' not in st.session_state:
    st.session_state.pali_input = ""

# අකුරක් එකතු කරන ශ්‍රිතය
def add_char(char):
    st.session_state.pali_input += char

# අකුරු බොත්තම් පෙළ
special_chars = ['ā', 'ī', 'ū', 'ṃ', 'ṇ', 'ṇḍ', 'ḷ', 'ṭ', 'ḍ', 'ñ', 'ṅ']
cols = st.columns(len(special_chars))

for i, char in enumerate(special_chars):
    if cols[i].button(char):
        add_char(char)

# පාලි පාඨය ඇතුළත් කරන කොටුව
# මෙහි value එක ලෙස session_state එක ලබා දී ඇත
pali_text = st.text_area(
    "පාලි වාක්‍යය මෙහි ඇතුළත් කරන්න:", 
    value=st.session_state.pali_input,
    height=150,
    placeholder="උදා: Sabbe satta bhavantu sukhitatta",
    key="text_input_area"
)

# පෙළ පිරිසිදු කරන බොත්තම
if st.button("පිරිසිදු කරන්න (Clear)"):
    st.session_state.pali_input = ""
    st.rerun()

st.markdown("---")

# 5. පරිවර්තනය කිරීමේ ක්‍රියාවලිය
if st.button("පරිවර්තනය කරන්න", type="primary"):
    if pali_text:
        with st.spinner('AI මගින් විශ්ලේෂණය කරමින් පවතී...'):
            try:
                prompt = (
                    f"You are a Pali language scholar. Translate the following text into "
                    f"clear Sinhala and English. Also, provide a word-by-word breakdown table.\n\n"
                    f"Pali Text: {pali_text}"
                )
                response = model.generate_content(prompt)
                st.markdown("### 📝 ප්‍රතිඵලය:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"පරිවර්තනය අසාර්ථක විය: {e}")
    else:
        st.warning("කරුණාකර පාලි පාඨයක් ඇතුළත් කරන්න.")

st.markdown("---")
st.caption("මෙම පද්ධතිය Google Gemini AI තාක්ෂණයෙන් ක්‍රියාත්මක වේ.")
