import time
# import pyttsx3
# import webbrowser
# import pywhatkit
import os
import sys
# from googlesearch import search
import google.generativeai as genai
# from langchain_google_genai import GoogleGenerativeAI
# from asr2 import asr
# from tts import tts
from dotenv import load_dotenv
load_dotenv()

query = sys.argv[1]
# engine = pyttsx3.init()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# ----------------------------TTS----------------------------
# def tts(text):
#     engine.say(text)
#     engine.runAndWait()

# -------------------As the generative output contains multiple *. So this function removes them-------------------
def preprocess(text):
    text = text.replace('*', '')
    return text


# --------------------Conversation Handling----------------------
def response(text):
  response = chat.send_message(text)
  response = preprocess(response.text)
  print(response)
#   tts(response)


# ---------------------Open Google--------------------------------
# def browse(url):
#     webbrowser.open_new(url)


# -----------------------Play Youtube video------------------------
# def play_on_youtube(query):
#     query = query.split("play ")[1]
#     query = query.split(" on youtube")[0]
#     print(f"Playing {query} on youtube.....")
#     # tts(f"Playing {query} on youtube.....")
#     pywhatkit.playonyt(query)


# ------------------------Search in Google--------------------------
# def search_on_google(text):
#     search_term = text.split("search for ")[1] if "search for " in text else text
#     print(f"Searching Google for : {search_term}")
#     # tts(f"{search_term}")
#     top_result = list(search(search_term, advanced=True))

#     print(f"Title : {top_result[0].title}")
#     print(f"Description : {top_result[0].description}")
#     # tts(f"{top_result[0].description}")

#     print("Would you like me to show you the results on web? (yes/no)")
#     # tts("Would you like me to show you the results on web?")
#     # show = asr()
#     show = input()
#     print("User : ", show)
#     if "yes" in show.lower():
#         browse(top_result[0].url)
#     else:
#         return

# =================================================================================================================
# -----------------------------Main Function----------------------------
def main(query):
    try:
        while True:
        #   user_input = asr()
          user_input = query
        #   print("User : ", user_input)

          if "stop" in user_input.lower() or "exit" in user_input.lower():
              break
        #   elif "search" in user_input.lower():
        #       search_on_google(user_input)
        #   elif "play" in user_input.lower() or "youtube" in user_input.lower():
        #       play_on_youtube(user_input)
        #       break
          else:
              response(user_input)
            #   time.sleep(2)

    except KeyboardInterrupt:
        print("Bye Bye....")

    except Exception as e:
        if e:
            print(e)
        else:
            # tts("Sorry I couldn't understand what you said.")
            print("Sorry I couldn't understand what you said.")
        

if __name__ == "__main__":
    main(query)
