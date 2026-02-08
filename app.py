import streamlit as st
import google.generativeai as genai

# API Key එක ආරක්ෂිතව Secrets හරහා ලබා ගැනීම
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key එක සම්බන්ධ ගැටලුවකි. කරුණාකර Secrets පරීක්ෂා කරන්න.")

st.set_page_config(page_title="AI පාලි පරිවර්තකය", page_icon="☸️")
st.title("☸️ AI පාලි පරිවර්තකය")

pali_text = st.text_area("පාලි වාක්‍යය ඇතුළත් කරන්න:", placeholder="උදා: Sabbe satta bhavantu sukhitatta")

if st.button("පරිවර්තනය කරන්න"):
    if pali_text:
        with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
            try:
                prompt = f"Pali scholar mode: Translate '{pali_text}' to Sinhala, English and give word meanings."
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"දෝෂයක්: {e}")
