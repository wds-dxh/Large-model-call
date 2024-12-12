from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class LLMBase(ABC):
    """LLM基类，定义统一接口"""
    
    @abstractmethod
    def initialize(self) -> None:
        """初始化LLM客户端"""
        pass
    
    @abstractmethod
    def chat(self, user_id: str, message: str, context: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """聊天接口"""
        pass
    
    @abstractmethod
    def update_settings(self, settings: Dict[str, Any]) -> None:
        """更新设置"""
        pass
    
    @abstractmethod
    def load_prompt(self, prompt_name: str) -> str:
        """加载提示词"""
        pass
    
    @abstractmethod
    def save_conversation(self, user_id: str, conversation: List[Dict]) -> None:
        """保存对话历史"""
        pass
    
    @abstractmethod
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """获取对话历史"""
        pass 