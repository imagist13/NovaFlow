"""小红书平台适配器."""

from typing import List
from pydantic import Field

from .base_platform import BasePlatform, PlatformConfig, PlatformContent
from ..core.llm_factory import LLMFactory


class XiaoHongShuPlatform(BasePlatform):
    """小红书平台适配器."""
    
    config = PlatformConfig(
        name="xiaohongshu",
        display_name="小红书",
        max_title_length=20,
        max_content_length=1000,
        min_content_length=50,
        allow_images=True,
        allow_hashtags=True,
        allow_mentions=True,
        require_title=True,
    )
    
    SYSTEM_PROMPT = """你是一个专业的小红书内容创作者，擅长创作吸引人的小红书笔记。
    
    小红书特点：
    - 标题简短有力，通常带有emoji
    - 内容以分享、种草为主
    - 善用emoji增加趣味性
    - 标签使用#号
    - 语气亲切、口语化
    
    请根据原始内容创作适合小红书风格的笔记。"""
    
    def __init__(self):
        self.llm = LLMFactory.get_llm()
    
    async def transform(self, source_content: str, **kwargs) -> PlatformContent:
        """转换为小红书格式."""
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """请将以下内容转换为小红书风格的笔记：

内容：{content}

请生成：
1. 一个吸引人的标题（20字以内，带emoji）
2. 正文内容（符合小红书风格）
3. 3-5个相关标签（用#号开头）

请以JSON格式输出：
{{"title": "标题", "content": "正文", "hashtags": ["#标签1", "#标签2"]}}
"""),
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"content": source_content})
        
        import json
        result = json.loads(response.content)
        
        return PlatformContent(
            title=result.get("title"),
            content=result.get("content", ""),
            hashtags=[tag.lstrip("#") for tag in result.get("hashtags", [])],
        )
    
    def transform_sync(self, source_content: str, **kwargs) -> PlatformContent:
        """同步转换为小红书格式."""
        import json
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """请将以下内容转换为小红书风格的笔记：

内容：{content}

请生成：
1. 一个吸引人的标题（20字以内，带emoji）
2. 正文内容（符合小红书风格）
3. 3-5个相关标签（用#号开头）

请以JSON格式输出：
{{"title": "标题", "content": "正文", "hashtags": ["#标签1", "#标签2"]}}
"""),
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"content": source_content})
        
        result = json.loads(response.content)
        
        return PlatformContent(
            title=result.get("title"),
            content=result.get("content", ""),
            hashtags=[tag.lstrip("#") for tag in result.get("hashtags", [])],
        )
    
    def validate(self, content: PlatformContent) -> bool:
        """验证内容."""
        if self.config.require_title and not content.title:
            return False
        if content.title and len(content.title) > self.config.max_title_length:
            return False
        if len(content.content) < self.config.min_content_length:
            return False
        if len(content.content) > self.config.max_content_length:
            return False
        return True
    
    def get_platform_rules(self) -> str:
        """获取平台规则."""
        return """
=== 小红书平台规则 ===
- 标题：20字以内，建议带emoji
- 正文：50-1000字，风格亲切、口语化
- 标签：使用#号，3-5个相关标签
- 图片：支持多图，建议9图
- 互动：善用emoji和表情增加趣味性
"""
