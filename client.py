import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="You are a virtual assistant named Jarvis skilled in general tasks like Alexa, Siri, and Google Assistant. You should always respond in the persona of Jarvis.",
)

completion = model.generate_content("what is coding?")

print(completion.text)
