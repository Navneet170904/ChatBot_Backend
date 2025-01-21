import time
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

query = sys.argv[1]

GOOGLE_API_KEY = os.environ.get("AIzaSyAFZ9kk_W9BocWFpfCtWsCAy9XQOCbxy7k")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

response = chat.send_message(query)
print(response.text)