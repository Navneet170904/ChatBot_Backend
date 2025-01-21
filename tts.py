import requests
from pydub import AudioSegment
from pydub.playback import play
import io
import os
from dotenv import load_dotenv

load_dotenv()


url = "https://api.elevenlabs.io/v1/text-to-speech/Aexa8w05NUs0Zjsr89r8"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": os.environ.get("xi-api-key")
}

def tts(text):
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
        }
    }

    response = requests.post(url, json=data, headers=headers)
    # with open('./output.mp3', 'wb') as f:
    #     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
    #         if chunk:
    #             f.write(chunk)

    audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    play(audio_segment)
    



