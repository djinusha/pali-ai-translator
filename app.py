import streamlit as st
import google.generativeai as genai

# UI සැකසුම
st.set_page_config(page_title="AI පාලි පරිවර්තකය", page_icon="☸️")

def get_working_model():
    """ඔබේ API Key එකට සහය දක්වන පවතින මාදිලියක් තෝරා දෙයි"""
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # වඩාත් සුදුසු මාදිලි පිළිවෙළින් පරීක්ෂා කරයි
    for model_name in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
        if model_name in available_models:
            return model_name
    return available_models[0] if available_models else None

# API Key එක Secrets හරහා ආරක්ෂිතව ලබා ගැනීම
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # පද්ධතියට ගැලපෙන මාදිලිය ස්වයංක්‍රීයව සොයා ගැනීම
    model_id = get_working_model()
    
    if model_id:
        model = genai.GenerativeModel(model_id)
    else:
        st.error("ඔබේ API Key එක සඳහා කිසිදු Gemini මාදිලියක් හමු නොවීය.")

except Exception as e:
    st.error(f"API සම්බන්ධ වීමේ ගැටලුවකි: {e}")

st.title("☸️ AI පාලි පරිවර්තකය")
st.markdown("---")

pali_text = st.text_area("පාලි වාක්‍යය මෙහි ඇතුළත් කරන්න:", 
                         placeholder="උදා: Sabbe satta bhavantu sukhitatta")

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
