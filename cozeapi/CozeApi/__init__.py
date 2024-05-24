'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-24 09:28:04
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-24 09:38:19
FilePath: /cozeapi/CozeApi/__init__.py
Description: 模块初始化文件
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''

""""
初始化文件的作用：
1. 用于标识当前文件夹是一个包

初始化文件的内容：
1. 可以为空
2. 可以包含当前包中所有模块的初始化代码, 例如导入模块、定义变量等
3. 可以包含当前包的作者、版本等信息
"""

# 导入模块
from .coze import coze_chat_api
from .get_content import get_first_message_content