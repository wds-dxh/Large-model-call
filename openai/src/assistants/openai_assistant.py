import json
import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from src.base.llm_base import LLMBase
from src.utils.config_loader import ConfigLoader

class OpenAIAssistant(LLMBase):
    def __init__(self, config_path: str = "config/config.json"):
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.get_config()
        self.client = None
        self.current_role = "default"
        self.conversation_context = {}
        self.max_turns = self.config.get('conversation', {}).get('max_turns', 10)
        self.truncate_mode = self.config.get('conversation', {}).get('truncate_mode', 'sliding')
        self.initialize()
        
    def initialize(self) -> None:
        """初始化OpenAI客户端"""
        self.client = OpenAI(
            api_key=self.config['openai']['api_key'],
            base_url=self.config['openai'].get('base_url', "https://api.chatanywhere.tech"),
            timeout=self.config['openai'].get('timeout', 30),  # 添加超时设置
        )
    
    @retry(         # 重试机制，使用装饰器retry
        stop=stop_after_attempt(3),  # 最多重试3次
        wait=wait_exponential(multiplier=1, min=4, max=10),  # 指数退避重试
        reraise=True
    )
    def _make_request(self, messages: List[Dict]) -> Dict:
        """发送请求到OpenAI API，带有重试机制"""
        try:
            response = self.client.chat.completions.create(
                model=self.config['openai']['model'],
                messages=messages,
                temperature=self.config['openai'].get('temperature', 0.7),
                max_tokens=self.config['openai'].get('max_tokens', 1000),
                top_p=self.config['openai'].get('top_p', 1.0)
            )
            return {"success": True, "data": response}
        except Exception as e:
            print(f"API request failed: {str(e)}")
            return {"success": False, "error": str(e)}

    '''
    description: 处理用户消息
    param {*} self
    param {str} user_id 用户ID
    param {str} message 用户消息
    param {Optional} role_type 指定的角色类型，如果为None则使用当前角色
    return {*}
    '''       
    def chat(self, user_id: str, message: str, role_type: Optional[str] = None) -> Dict[str, Any]:
        """
        处理用户消息
        Args:
            user_id: 用户ID
            message: 用户消息
            role_type: 指定的角色类型，如果为None则使用当前角色
        """
        try:
            # 如果指定了新的角色类型，就更新当前角色
            if role_type and role_type != self.current_role:
                if not self.set_role(role_type):
                    return {
                        "error": f"无效的角色类型: {role_type}",
                        "timestamp": datetime.now().isoformat()
                    }

            # 获取当前角色的提示词
            system_prompt = self.load_prompt(self.current_role)
            
            # 获取或初始化用户的上下文
            if user_id not in self.conversation_context:
                self.conversation_context[user_id] = [{"role": "system", "content": system_prompt}]
            else:
                # 更���system message如果角色改变了
                if self.conversation_context[user_id][0]["role"] == "system":
                    self.conversation_context[user_id][0]["content"] = system_prompt
                else:
                    self.conversation_context[user_id].insert(0, {"role": "system", "content": system_prompt})
            
            # 在添加新消息前检查并截断上下文
            if user_id in self.conversation_context:
                self.conversation_context[user_id] = self._truncate_context(
                    self.conversation_context[user_id]
                )
            
            # 添加用户消息
            self.conversation_context[user_id].append({"role": "user", "content": message})
            
            # 使用重试机制发送请求
            response = self._make_request(self.conversation_context[user_id])
            
            if not response["success"]:
                return {
                    "error": response["error"],
                    "timestamp": datetime.now().isoformat()
                }
            
            assistant_message = response["data"].choices[0].message.content
            self.conversation_context[user_id].append({"role": "assistant", "content": assistant_message})
            
            # 保存对话历史
            self.save_conversation(user_id, self.conversation_context[user_id])
            
            return {
                "response": assistant_message,
                "timestamp": datetime.now().isoformat(),
                "current_role": self.current_role
            }
            
        except Exception as e:
            print(f"Chat error: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "current_role": self.current_role
            }
    
    def _load_prompts(self) -> Dict[str, str]:
        """加载提示词模板"""
        with open(self.config['storage']['prompts_path'], 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def load_prompt(self, prompt_name: str) -> str:
        """获取特定提示词"""
        prompts = self._load_prompts()
        return prompts.get(prompt_name, "")
        
    def update_settings(self, settings: Dict[str, Any]) -> None:
        """更新配置"""
        if 'max_turns' in settings:
            self.max_turns = settings['max_turns']
        if 'truncate_mode' in settings:
            if settings['truncate_mode'] not in ['sliding', 'clear']:
                raise ValueError("truncate_mode must be 'sliding' or 'clear'")
            self.truncate_mode = settings['truncate_mode']
        
        # 更新OpenAI相关配置
        openai_settings = {k: v for k, v in settings.items() 
                         if k not in ['max_turns', 'truncate_mode']}
        if openai_settings:
            self.config_loader.update_config({'openai': openai_settings})
            self.config = self.config_loader.get_config()
    
    '''
    description: 保存对话历史到JSON文件
    param {*} self
    param {str} user_id 用户ID
    param {List} conversation 对话历史
    return {*}
    '''    
    def save_conversation(self, user_id: str, conversation: List[Dict]) -> None:
        """保存对话历史到JSON文件"""
        try:
            with open(self.config['storage']['conversations_path'], 'r+', encoding='utf-8') as f:
                try:
                    conversations = json.load(f)
                except json.JSONDecodeError:
                    conversations = {}
                    
                conversations[user_id] = conversations.get(user_id, []) + [{    # 将新的对话历史添加到现有对话历史中
                    "timestamp": datetime.now().isoformat(),
                    "messages": conversation
                }]
                
                f.seek(0)
                json.dump(conversations, f, ensure_ascii=False, indent=2)
                f.truncate() # 截断文件
                
        except FileNotFoundError:
            with open(self.config['storage']['conversations_path'], 'w', encoding='utf-8') as f:
                json.dump({user_id: [{
                    "timestamp": datetime.now().isoformat(),
                    "messages": conversation
                }]}, f, ensure_ascii=False, indent=2)
                
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """获取用户对话历史"""
        try:
            with open(self.config['storage']['conversations_path'], 'r', encoding='utf-8') as f:
                conversations = json.load(f)
                return conversations.get(user_id, [])
        except FileNotFoundError:
            return [] 

    def set_role(self, role_type: str) -> bool:
        """
        设置AI助手的角色
        Args:
            role_type: 角色类型 (default/professional/creative/code/academic)
        Returns:
            bool: 是否成功设置角色
        """
        try:
            prompt = self.load_prompt(role_type)
            if prompt:
                self.current_role = role_type
                return True
            return False
        except Exception as e:
            print(f"设置角色失败: {str(e)}")
            return False

    def get_current_role(self) -> str:
        """获取当前角色类型"""
        return self.current_role

    def list_available_roles(self) -> List[str]:
        """获取所有可用的角色类型"""
        try:
            prompts = self._load_prompts()
            return list(prompts.keys())
        except Exception:
            return ["default"]  # 如果加载失败，至少返回默认角色

    def clear_context(self, user_id: str) -> None:
        """清除指定用户的对话上下文"""
        if user_id in self.conversation_context:
            del self.conversation_context[user_id]

    def get_current_context(self, user_id: str) -> Optional[List[Dict]]:
        """获取指定用户的当前对话上下文"""
        return self.conversation_context.get(user_id)

    def clear_all_contexts(self) -> None:
        """清除所有用户的对话上下文"""
        self.conversation_context.clear()

    def get_context_summary(self, user_id: str) -> Dict[str, Any]:
        """获取用户对话上下文的摘要信息"""
        context = self.conversation_context.get(user_id)
        if not context:
            return {
                "message_count": 0,
                "has_context": False,
                "max_turns": self.max_turns,
                "current_turns": 0
            }
        
        current_turns = (len(context) - 1) // 2  # 不计算system消息
        
        return {
            "message_count": len(context) - 1,
            "has_context": True,
            "current_role": self.current_role,
            "last_message_time": datetime.now().isoformat(),
            "max_turns": self.max_turns,
            "current_turns": current_turns
        }

    def _truncate_context(self, context: List[Dict]) -> List[Dict]:
        """
        截断对话上下文
        Args:
            context: 当前上下文
        Returns:
            截断后的上下文
        """
        if len(context) <= 1:  # 只有system消息
            return context
            
        # 计算实际对话轮数（不包括system消息）
        turns = (len(context) - 1) // 2  # 每轮包含一个user消息和一个assistant消息
        
        if turns <= self.max_turns:
            return context
            
        if self.truncate_mode == 'clear':
            # 保留system消息，清除其他所有消息
            return [context[0]]
        else:  # sliding mode
            # 保留system消息和最近的max_turns轮对话
            preserved_messages_count = self.max_turns * 2  # 每轮2条消息
            return [context[0]] + context[-preserved_messages_count:]