'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-12 16:42:59
Description: 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
from openai import OpenAI


client = OpenAI(api_key="sk-PLvmgppR3434WqQI5vo0wgxB9FkFwzwXuomR3dFQnO7H2cp1", base_url="https://api.chatanywhere.tech")

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