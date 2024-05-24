'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-21 20:39:38
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-24 19:01:54
FilePath: /kimi/test.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
from openai import OpenAI
 
client = OpenAI(
    api_key = "sk-afn5NxpCGr8PqEeCdkDQ4XYTWNv7BZFxCeE14WAdJudv5k6l",
    base_url = "https://api.moonshot.cn/v1",
)
 
completion = client.chat.completions.create(
    model = "moonshot-v1-8k",
    messages = [
        {"role": "system", "content": "您好，我是医学咨询助手，了解了您的病情描述后，我会基于医学知识为您提供专业的建议。请详细描述您当前的症状、已知的诊断信息以及任何测试结果，这样我可以更准确地帮助您。同时，我可以提供一些通用的建议或简单的方法来帮助您缓解症状，但请记得，这些信息不替代专业医疗意见，您应当咨询合格的医疗服务提供者以获得适当的诊断与治疗"},
        {"role": "user", "content": "我的脑袋有点痛怎么办？"},
    ],
    temperature = 0.3,
)
 
print(completion.choices[0].message.content)