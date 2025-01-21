import os
import speech_recognition as sr
from faster_whisper import WhisperModel

model_size = "large-v3"
recognizer = sr.Recognizer()

model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe(audio_file):
    segments, info = model.transcribe(f"./{audio_file}", beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        return(segment.text)
    
def asr():
    try:
        while True:
            with sr.Microphone() as source:
              print("Listening...")
              audio = recognizer.listen(source)

            audio_file = "temp_chunk.wav"

            with open(audio_file, "wb") as file:
              file.write(audio.get_wav_data())
              
            transcription = transcribe(audio_file)
            os.remove(audio_file)

            return(transcription)
        
    except KeyboardInterrupt:
        print("Stopping...")
