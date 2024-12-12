import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        load_dotenv()
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载并验证配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # 验证必要的配置项
        required_keys = ['openai', 'storage', 'conversation']
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required configuration key: {key}")
        
        # 替换环境变量
        config['openai']['api_key'] = os.getenv('OPENAI_API_KEY')
        
        # 确保存储路径存在
        for path_key in ['conversations_path', 'prompts_path']:
            data_dir = os.path.dirname(config['storage'][path_key])
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                
        return config
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        return self.config
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """更新配置"""
        for key, value in updates.items():
            if key in self.config:
                self.config[key].update(value) 