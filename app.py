import streamlit as st
import google.generativeai as genai

# පිටුවේ සැකසුම්
st.set_page_config(page_title="AI පාලි පරිවර්තකය", page_icon="☸️")

def get_working_model():
    """ඔබේ API Key එකට සහය දක්වන පවතින මාදිලියක් ස්වයංක්‍රීයව සොයා දෙයි"""
    try:
        # පවතින සියලුම මාදිලි පරීක්ෂා කරයි
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # අපට අවශ්‍ය මාදිලි ප්‍රමුඛතාවය අනුව පරීක්ෂා කරයි
        # මෙහිදී models/gemini-1.5-flash හෝ models/gemini-pro වැනි ඕනෑම එකක් තෝරාගනී
        for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']:
            if preferred in available_models:
                return preferred
        
        # ඉහත කිසිවක් නැත්නම් පවතින පළමු මාදිලිය ලබා දෙයි
        return available_models[0] if available_models else None
    except:
        return None

# --- API ආරක්ෂාව සහ සම්බන්ධතාවය ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        
        # වැඩ කරන මාදිලියක් ස්වයංක්‍රීයව ලබා ගැනීම
        working_model_id = get_working_model()
        
        if working_model_id:
            model = genai.GenerativeModel(working_model_id)
            # st.info(f"සක්‍රීය මාදිලිය: {working_model_id}") # අවශ්‍ය නම් මෙය පෙන්විය හැක
        else:
            st.error("ඔබේ API Key එක සඳහා කිසිදු මාදිලියක් හමු නොවීය.")
    else:
        st.error("GEMINI_API_KEY රහස් පදය (Secret) හමු නොවීය.")
except Exception as e:
    st.error(f"දෝෂයක් සිදු විය: {e}")

st.title("☸️ AI පාලි පරිවර්තකය")
st.markdown("---")

pali_text = st.text_area("පාලි වාක්‍යය මෙහි ඇතුළත් කරන්න:", placeholder="උදා: Sabbe satta bhavantu sukhitatta")

if st.button("පරිවර්තනය කරන්න"):
    if pali_text:
        with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
            try:
                prompt = f"As a Pali scholar, translate this to Sinhala and English with word meanings: {pali_text}"
                response = model.generate_content(prompt)
                st.markdown("### 📝 ප්‍රතිඵලය:")
                st.write(response.text)
            except Exception as e:
                st.error(f"පරිවර්තනය අසාර්ථක විය: {e}")
    else:
        st.warning("කරුණාකර පාලි වාක්‍යයක් ඇතුළත් කරන්න.")
