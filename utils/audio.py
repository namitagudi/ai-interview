import os
import whisper

@st_cache = None # Loaded dynamically in app.py via st.cache_resource

def process_audio(audio_bytes, whisper_model) -> dict:
    temp_path = "temp_recording.wav"
    with open(temp_path, "wb") as f:
        f.write(audio_bytes.read())

    result = whisper_model.transcribe(temp_path)
    transcript = result.get("text", "").strip()
    
    # Calculate audio duration and speech cadence (WPM)
    segments = result.get("segments", [])
    duration = segments[-1]["end"] if segments else 1.0
    words = len(transcript.split())
    wpm = round((words / duration) * 60, 2) if duration > 0 else 0.0

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return {
        "transcript": transcript,
        "word_count": words,
        "duration_sec": duration,
        "wpm": wpm
    }
