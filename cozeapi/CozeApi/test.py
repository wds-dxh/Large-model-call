'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-24 09:45:36
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-24 09:48:27
FilePath: /cozeapi/CozeApi/test.py
Description: coze官方使用的是curl演示，这里使用python的requests库来实现流式和非流式的聊天
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import requests
import json

class CozeAPI:

    def __init__(self, access_token, base_url="https://api.coze.com/open_api/v2/chat"):
        self.access_token = access_token
        self.base_url = base_url

    def chat_api(self, conversation_id, bot_id, user, query, stream=False):
        headers = {
            'Authorization': f"Bearer {self.access_token}",
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'api.coze.com'
        }

        payload = json.dumps({
            "conversation_id": conversation_id,
            "bot_id": bot_id,
            "user": user,
            "query": query,
            "stream": stream
        })

        response = requests.post(self.base_url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()
        else:
            # Handle error
            return response.text

    def stream_chat(self, conversation_id, bot_id, user, query):
        headers = {
            'Authorization': f"Bearer {self.access_token}",
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'api.coze.com'
        }

        data = json.dumps({
            "conversation_id": conversation_id,
            "bot_id": bot_id,
            "user": user,
            "query": query,
            "stream": True
        })

        with requests.post(self.base_url, headers=headers, data=data, stream=True) as response:
            if response.encoding is None:
                response.encoding = 'utf-8'

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    print(line)  # 或者处理 line
                    # 例如解析 JSON 并获取消息内容
                    parsed_line = json.loads(line)
                    message = parsed_line.get('message')
                    if message:
                        print(message)

    # Allows changing the URL if needed
    def set_base_url(self, base_url):
        self.base_url = base_url


if __name__ == "__main__":
    coze = CozeAPI(access_token="pat_L9hB7wpvvH3yU4xmEsYErwgoSZQAdRrq7bgLTIgcVxl3HFJwhfsOHkxZLVoCPAmB")
    # 以下部分是可选的，如果你需要使用不同的 URL
    # coze.set_base_url("https://new.api.coze.com/open_api/v2/chat")

    response_data = coze.chat_api(
        conversation_id="123",
        bot_id="7361974174858461190",
        user="wds",
        query="你是谁？",
        stream=False
    )
    print(response_data)

    # If you want to test the streaming functionality
    # coze.stream_chat(
    #     conversation_id="123",
    #     bot_id="7361974174858461190",
    #     user="wds",
    #     query="你是谁？"
    # )