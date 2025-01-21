import speech_recognition as sr
import os
import whisper

models = ["base", "small", "medium", "large"]

model = whisper.load_model(models[1])
recognizer = sr.Recognizer()

def transcribe(model, audio_file):
    audio = whisper.load_audio(audio_file)
    result = model.transcribe(audio)
    return result["text"]


def asr():
    try:
        while True:
            with sr.Microphone() as source:
              print("Listening...")
              audio = recognizer.listen(source)

            audio_file = "temp_chunk.wav"

            with open(audio_file, "wb") as file:
              file.write(audio.get_wav_data())
              
            transcription = transcribe(model, audio_file)
            os.remove(audio_file)

            return(transcription)
        
    except KeyboardInterrupt:
        print("Stopping...")