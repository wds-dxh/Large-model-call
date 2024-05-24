'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-24 09:27:06
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-24 10:17:36
FilePath: /cozeapi/CozeApi/coze.py
Description: coze官方使用的是curl演示，这里使用python的requests库来实现
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import time
import requests
import json
from get_content import get_first_message_content as get_content
def coze_chat_api(conversation_id, bot_id, user, query, stream=False, access_token="your_access_token"):
    url = "https://api.coze.com/open_api/v2/chat"
    
    headers = {
        'Authorization': f"Bearer {access_token}",
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
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        # Handle error
        return response.text
    

def stream_coze_chat(conversation_id, bot_id, user, query, access_token):
    url = "https://api.coze.com/open_api/v2/chat"

    headers = {
        'Authorization': f"Bearer {access_token}",
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

    with requests.post(url, headers=headers, data=data, stream=True) as response:
        if response.encoding is None:
            response.encoding = 'utf-8'

        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(line)  # 或者处理 line




if __name__ =="__main__":
    # 使用该函数（将 'your_access_token' 替换为你的真实 access token）
    now = time.time()
    response_data = coze_chat_api(
        conversation_id="123",
        bot_id="7361974174858461190",
        user="wds",
        query="你是谁？",
        stream=False,
        access_token="pat_L9hB7wpvvH3yU4xmEsYErwgoSZQAdRrq7bgLTIgcVxl3HFJwhfsOHkxZLVoCPAmB"
    )
    message = get_content(response_data)
    requests_time = time.time() - now
    print(f"requests_time: {requests_time}")
    print(message)


