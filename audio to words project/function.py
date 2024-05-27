import speech_recognition as sr
from pydub import AudioSegment
import io
import os

r = sr.Recognizer()

def record_transcribe():
    text = ""
    audio = None
    with sr.Microphone() as source:
        print('Listening...')
        r.adjust_for_ambient_noise(source, duration=0.5)
        while True:
            try:
                audio = r.listen(source, timeout=None)
                text = r.recognize_google(audio)
                print(text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
                break
            return text, audio

def output_text(text, filename):
    with open(filename, "a") as f:
        f.write(text)
        f.write('\n')

def save_audio_as_mp3(audio, filename):
    if audio is not None:
        audio_data = audio.get_wav_data()
        audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
        audio_segment.export(filename, format="mp3")

def get_next_session_id():
    session_id = 1
    while os.path.exists(f"session_{session_id}_transcriptions.txt"):
        session_id += 1
    return session_id

def save_transcriptions_for_session(session_id, text, audio):
    text_filename = f"session_{session_id}_transcriptions.txt"
    audio_filename = f"session_{session_id}_audio_{get_audio_counter(session_id)}.mp3"

    output_text(text, text_filename)

    save_audio_as_mp3(audio, audio_filename)

def get_audio_counter(session_id):
    counter = 1
    while os.path.exists(f"session_{session_id}_audio_{counter}.mp3"):
        counter += 1
    return counter
