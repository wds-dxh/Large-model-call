import time
from CozeApi.coze import coze_chat_api
from CozeApi.get_content import get_first_message_content



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
    message = get_first_message_content(response_data)
    requests_time = time.time() - now
    print(f"requests_time: {requests_time}")
    print(message)