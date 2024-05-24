'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-07 11:26:16
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-07 11:26:26
FilePath: /openai/test.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
from openai import OpenAI       #pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple
import pyttsx3      

class HealthAdviceAssistant:
    def __init__(self, api_key, base_url="https://api.nextapi.fun/v1", model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.speech_engine = pyttsx3.init()

    def get_health_advice(self, fruit_type):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "食物识别与健康建议：1.用户给出实物名称，你来给用户提供有关这个食物的健康建议。2.分点给出，让用户更明确，帮助用户更健康地享用这个食物。3.内容简洁明了，内容不要太多了，少于100字！！！。4.注意给出注意事项，内容要温暖，不要太机械了，给使用者家的感觉"},
                {"role": "user", "content": fruit_type}
            ],
            stream=True,
            model="gpt-3.5-turbo",
        )

        advice_text = ''
        for chunk in chat_completion:
            content_part = chunk.choices[0].delta.content
            if content_part is not None:
                advice_text = advice_text + content_part
                print(content_part, end="")

        self.speech_engine.say(advice_text)
        self.speech_engine.runAndWait()

if __name__ == "__main__":
    api_key = "ak-COVDNhZt8spc38GSRCPbi6IPbvH9EghL6pEfibt3uz8i87tE"  # Replace with your actual API key
    assistant = HealthAdviceAssistant(api_key)

    # Example usage
    fruit_type = "我今天有点咳嗽了,需要按摩哪个穴位呢？"
    assistant.get_health_advice(fruit_type)
