'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-24 09:35:58
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-24 10:17:08
FilePath: /cozeapi/CozeApi/get_content.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
def get_first_message_content(response_data):
    if 'messages' in response_data and len(response_data['messages']) > 0:
        return response_data['messages'][0]['content']
    else:
        return "No content found."

if __name__ == '__main__':
    # 假设 response_data 是 API 响应的字典
    response_data = {
        'messages': [
            {'role': 'assistant', 'type': 'answer', 'content': '您好！我是专门提供计算机科学相关知识和信息的专家...', 'content_type': 'text'},
            # ... 其他消息 ...
        ],
        'conversation_id': '123',
        'code': 0,
        'msg': 'success'
    }

    # 使用以上定义的函数获取第一个 content
    first_content = get_first_message_content(response_data)
    print(first_content)