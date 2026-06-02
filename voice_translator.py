import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
import gtts
import io
import base64
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title='AI_Translator',page_icon='🎤',layout='wide')
st.title("Voice Translator")

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
col1,col2 = st.columns(2)
with col1:
    st.subheader("English")
    audio_bytes = audio_recorder(
    text="Click to record", 
    recording_color="#e81416", 
    neutral_color="#6aa36f"
)
    if audio_bytes:
        r=sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        st.text('say something...')
        r.adjust_for_ambient_noise(audio_bytes, duration=1)
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)
                st.session_state.input_text = r.recognize_google(audio)
    
            # translator=GoogleTranslator(source='auto',target='hi')
            # st.session_state.translated_text = translator.translate(st.session_state.input_text)
        except Exception as e:
            st.error("your voice not clear Try again!")
    typed_text=st.text_area("Input Text", value=st.session_state.input_text, height=150)
    if typed_text != st.session_state.input_text:
        st.session_state.input_text = typed_text

    if st.session_state.input_text:
        try:
            translator = GoogleTranslator(source='auto',target='hi')
            st.session_state.translated_text = translator.translate(st.session_state.input_text)
        except Exception as e:
            st.session_state.translated_text = "Translation error."
    else:
        st.session_state.translated_text = ""
with col2:
    st.subheader("Hindi")
    st.write("")
    st.text_area("Translator",value=st.session_state.translated_text,height=150)
    if st.session_state.translated_text:
        try:
            tts=gtts.gTTS(text=st.session_state.translated_text,lang='hi')
            fp=io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_byte=fp.read()
            b64_audio=base64.b64encode(audio_byte).decode()

           

            audio_html=f"""
                <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
                    <button onclick="document.getElementById('hindi_audio').play()" 
                            style="background: none; border: none; font-size: 28px; cursor: pointer; padding: 0; line-height: 1;">
                        🔊
                    </button>
                    <span style="font-size: 14px; color: #888; user-select: none;">
                        Click icon to replay
                    </span>
                    <audio id="hindi_audio" autoplay="true" style="display: none;">
                        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                    </audio>
                </div>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

            #st.audio(fp,format='audio/mp3')
        except Exception as e:
            st.error(f"Audio display error : {e}")
    
