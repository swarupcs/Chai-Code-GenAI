from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini client
genai.configure(api_key=api_key)

# Use the model
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Why is the sky blue?")
print(response.text)
