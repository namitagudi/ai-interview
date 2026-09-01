import whisper

def verifyandtranscribeaudio(audiofilepath):
    model = whisper.load_model("base")
    result = model.transcribe(audiofilepath)
    transcripttext = result["text"]
    
    wordlist = transcripttext.split()
    totalwords = len(wordlist)
    
    if totalwords < 10:
        return {
            "passed": False,
            "text": transcripttext,
            "count": totalwords,
            "message": "Your answer was not detailed enough. Please expand your response to improve it."
        }
        
    return {
        "passed": True,
        "text": transcripttext,
        "count": totalwords,
        "message": "Answer accepted successfully."
    }
