from openai import OpenAI
import pyttsx3  # 导入库
# OpenAI.api_base = "https://api.nextapi.fun/v1"
# OpenAI.api_key = "ak-COVDNhZt8spc38GSRCPbi6IPbvH9EghL6pEfibt3uz8i87tE"
client = OpenAI(
    api_key = "ak-COVDNhZt8spc38GSRCPbi6IPbvH9EghL6pEfibt3uz8i87tE",
    base_url = "https://api.nextapi.fun/v1",
    )

# Example OpenAI Python library request
chat_completion = client.chat.completions.create(
    messages=[
    {"role": "system", "content": "食物识别与健康建议：1.用户给出实物名称，你来给用户提供有关这个食物的健康建议。2.分点给出，让用户更明确，帮助用户更健康地享用这个食物。3.内容简洁明了，内容不要太多了，少于100字！！！。4.注意给出注意事项，内容要温暖，不要太机械了，给使用者家的感觉"},
    {"role": "user", "content": "苹果!"}
    ],
    stream=True,
    model="gpt-3.5-turbo",
)
# print(chat_completion)
# assistant_reply = chat_completion.choices[0].message.content
# print(assistant_reply)

say_str = ''
say_eng = pyttsx3.init()  # 初始化一个实例
# Process and print content from streaming chunks
for chunk in chat_completion:
    content_part = chunk.choices[0].delta.content
    if content_part is not None:
        say_str = say_str + content_part
        print(content_part, end="")  # Use space as the separator


say_eng.say(say_str)
say_eng.runAndWait()  # 运行并处理语音命令
