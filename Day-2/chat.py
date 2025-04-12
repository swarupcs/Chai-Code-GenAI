from dotenv import load_dotenv
from openai import OpenAI
 
load_dotenv()
 
client = OpenAI()
 
result = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        { "role": "user", "content": "What is greator? 9.8 or 9.11" } # Zero Shot Prompting
    ]
)
 
print(result.choices[0].message.content)