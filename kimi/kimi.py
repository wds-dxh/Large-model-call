'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-24 20:27:44
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-24 20:30:00
FilePath: /kimi/kimi.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
from openai import OpenAI

class OpenAIChatClient:
    def __init__(self, api_key, model="moonshot-v1-8k", base_url="https://api.moonshot.cn/v1"):
        """
        创建一个 OpenAI 聊天客户端对象。
        
        :param api_key: 用户 OpenAI API 的密钥。
        :param model: 要使用的模型名称，有默认值。
        :param base_url: API 的基地址，有默认值。
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model
        
    def ask(self, user_message, temperature=0.3):
        """
        用户直接输入问题，函数内部生成聊天信息列表并调用模型得到答案。
        
        :param user_message: 用户想要提问的内容。
        :param temperature: 可选参数，设置此次会话的 temperature。
        :return: 返回模型的回答内容。
        """
        messages = [
            {"role": "user", "content": user_message},
        ]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        
        return completion.choices[0].message.content

if __name__ == "__main__":  
    api_key = "sk-afn5NxpCGr8PqEeCdkDQ4XYTWNv7BZFxCeE14WAdJudv5k6l"
    model = "moonshot-v1-8k"    
    base_url = "https://api.moonshot.cn/v1"
    chat_client = OpenAIChatClient(api_key, model, base_url)

    user_message = "这里是我想要提问的具体问题。"
    response = chat_client.ask(user_message)
    print(response)