from function import *

session_id = get_next_session_id()

while(1):
    text, audio = record_transcribe()
    if text and audio:
        save_transcriptions_for_session(session_id, text, audio)