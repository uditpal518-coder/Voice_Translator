import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
import gtts
import io
import base64
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title='AI_Translator',page_icon='🎤',layout='wide')
st.title("Voice Translator")

INPUT_LANGUAGES = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Spanish": "es-ES",
    "French": "fr-FR"
}
LANGUAGES = {
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Arabic": "ar",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "English": "en"
}

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
col1,col2 = st.columns(2)
with col1:
    target_lang_name = st.selectbox("Select Target Language:", list(INPUT_LANGUAGES.keys()))
    input_lang = LANGUAGES[target_lang_name] 
    st.subheader(target_lang_name)
    audio_bytes = audio_recorder(
    text="Click to record", 
    recording_color="#e81416", 
    neutral_color="#6aa36f"
)
    if audio_bytes:
        r=sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        st.text('Processing audio...')
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)
                st.session_state.input_text = r.recognize_google(audio_data, language=input_lang)
    
            # translator=GoogleTranslator(source='auto',target='hi')
            # st.session_state.translated_text = translator.translate(st.session_state.input_text)
        except Exception as e:
            st.error("your voice not clear Try again!")
    st.text_area("Input Text",value=st.session_state.input_text,height=150)

with col2:

    target_lang_name = st.selectbox("Select Target Language:", list(LANGUAGES.keys()))
    target_lang = LANGUAGES[target_lang_name] 
    
    st.subheader(target_lang_name)
    st.write("")
    if st.session_state.input_text:
        try:
            # Automatic source detect karke target mein translate karega
            translator = GoogleTranslator(source='auto', target=target_lang)
            st.session_state.translated_text = translator.translate(st.session_state.input_text)
        except Exception as e:
            f"Translation error: {e}"
    st.text_area("Translator",value=st.session_state.translated_text,height=150)
    if st.session_state.translated_text:
        try:
            tts=gtts.gTTS(text=st.session_state.translated_text,lang=target_lang)
            fp=io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_byte=fp.read()

            st.audio(fp, format='audio/mpeg', autoplay=True)
        except Exception as e:
            st.error(f"Audio display error : {e}")
    
