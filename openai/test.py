import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)
client = OpenAI(api_key=api_key, base_url="https://api.chatanywhere.tech")

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "你是谁."
        }
    ]
)

print(completion.choices[0].message)