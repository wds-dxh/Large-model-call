# OpenAI Assistant 类说明文档

## 概述

`OpenAIAssistant` 类提供了一个封装的接口来与OpenAI的API进行交互，支持多角色对话、上下文管理、对话历史存储等功能。该类继承自`LLMBase`抽象基类，提供了统一的接口规范，便于扩展其他大语言模型的实现。

## 主要功能

- 多角色对话：支持多种预定义角色，如专业助手、创意助手、代码助手等
- 上下文管理：自动维护对话上下文，支持上下文长度限制
- 对话历史：将对话历史保存到JSON文件，支持查询历史对话
- 配置管理：支持通过配置文件和环境变量管理API密钥等设置
- 错误处理：内置重试机制和错误处理
- 可扩展性：基于抽象基类设计，便于扩展其他模型

## 核心方法介绍

### 构造函数

```python
def __init__(self, config_path: str = "config/config.json")
```

- **简介**：初始化OpenAI Assistant实例
- **参数**：
  - `config_path`：配置文件路径，默认为"config/config.json"
- **功能**：
  - 加载配置文件
  - 初始化OpenAI客户端
  - 设置对话上下文管理
  - 配置对话轮数限制

### 聊天方法

```python
def chat(self, user_id: str, message: str, role_type: Optional[str] = None) -> Dict[str, Any]
```

- **简介**：处理用户消息并返回AI响应
- **参数**：
  - `user_id`：用户标识符
  - `message`：用户消息内容
  - `role_type`：可选的角色类型
- **返回值**：包含响应内容、时间戳和当前角色的字典
- **功能**：
  - 维护对话上下文
  - 自动截断过长对话
  - 保存对话历史
  - 支持角色切换

### 角色管理

```python
def set_role(self, role_type: str) -> bool
def get_current_role(self) -> str
def list_available_roles(self) -> List[str]
```

- **简介**：管理AI助手的角色
- **功能**：
  - 切换当前角色
  - 获取当前角色
  - 列出所有可用角色

### 上下文管理

```python
def clear_context(self, user_id: str) -> None
def get_current_context(self, user_id: str) -> Optional[List[Dict]]
def get_context_summary(self, user_id: str) -> Dict[str, Any]
```

- **简介**：管理对话上下文
- **功能**：
  - 清除指定用户的上下文
  - 获取当前上下文
  - 获取上下文摘要信息

## 配置文件说明

配置文件(config.json)包含以下主要部分：

```json
{
    "openai": {
        "api_key": "${OPENAI_API_KEY}",
        "base_url": "https://api.chatanywhere.tech",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "storage": {
        "conversations_path": "data/conversations.json",
        "prompts_path": "data/prompts.json"
    },
    "conversation": {
        "max_turns": 10,
        "truncate_mode": "sliding"
    }
}
```

## 使用示例

```python
from src.assistants.openai_assistant import OpenAIAssistant

# 初始化助手
assistant = OpenAIAssistant()

# 发送消息
response = assistant.chat("user123", "你好")
print(response["response"])

# 切换角色
assistant.set_role("professional")
response = assistant.chat("user123", "解释量子力学")

# 查看上下文信息
context_summary = assistant.get_context_summary("user123")
print(context_summary)
```

## 注意事项

1. **API密钥**：确保在.env文件中设置了正确的OPENAI_API_KEY
2. **存储路径**：确保data目录存在且有写入权限
3. **角色定义**：在prompts.json中定义新的角色提示词
4. **上下文限制**：注意设置合适的max_turns以避免token超限
5. **错误处理**：建议实现适当的错误处理机制

## 扩展开发

要实现新的LLM模型支持，需要：

1. 继承LLMBase抽象基类
2. 实现所有��象方法
3. 在配置文件中添加相应配置
4. 确保实现了必要的错误处理和重试机制

## 依赖要求

```text
openai>=1.0.0
pydantic>=2.0.0
python-dotenv>=0.19.0
tenacity>=8.0.0
``` 