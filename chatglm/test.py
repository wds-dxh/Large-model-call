from zhipuai import ZhipuAI

client = ZhipuAI(api_key="334f9bba3a40a758ae8586464a77698a.QCIwFck36K2xVGYN") # 请填写您自己的APIKey

response = client.chat.completions.create(
    model="glm-3-turbo", # 填写需要调用的模型名称
    messages = [
        {
            "role": "user",
            "content": "你能帮我查询2024年1月1日从北京南站到上海的火车票吗？"
        }
    ],
    tools = [
        {
            "type": "function",
            "function": {
                "name": "query_train_info",
                "description": "根据用户提供的信息，查询对应的车次",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "departure": {
                            "type": "string",
                            "description": "出发城市或车站",
                        },
                        "destination": {
                            "type": "string",
                            "description": "目的地城市或车站",
                        },
                        "date": {
                            "type": "string",
                            "description": "要查询的车次日期",
                        },
                    },
                    "required": ["departure", "destination", "date"],
                },
            }
        }
    ],
    tool_choice="auto",
)
print(response.choices[0].message)