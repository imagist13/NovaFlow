"""知乎平台适配器."""

from typing import List
from pydantic import Field

from .base_platform import BasePlatform, PlatformConfig, PlatformContent
from ..core.llm_factory import LLMFactory


class ZhiHuPlatform(BasePlatform):
    """知乎平台适配器."""
    
    config = PlatformConfig(
        name="zhihu",
        display_name="知乎",
        max_title_length=50,
        max_content_length=5000,
        min_content_length=100,
        allow_images=True,
        allow_hashtags=True,
        allow_mentions=True,
        require_title=True,
    )
    
    SYSTEM_PROMPT = """你是一个专业的知乎内容创作者，擅长创作高质量的知识分享内容。
    
    知乎特点：
    - 标题可以是问句或陈述句，要有信息量
    - 内容专业、深度、有见地
    - 善用结构化表达（列表、分点）
    - 标签使用#号
    - 语气严谨但不失趣味
    
    请根据原始内容创作适合知乎风格的文章。"""
    
    def __init__(self):
        self.llm = LLMFactory.get_llm()
    
    async def transform(self, source_content: str, **kwargs) -> PlatformContent:
        """转换为知乎格式."""
        from langchain_core.prompts import ChatPromptTemplate
        import json
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """请将以下内容转换为知乎风格的深度文章：

内容：{content}

请生成：
1. 一个有信息量的标题（50字以内）
2. 深度正文内容（使用结构化表达，分点说明）
3. 2-4个相关话题标签

请以JSON格式输出：
{{"title": "标题", "content": "正文", "hashtags": ["#话题1", "#话题2"]}}
"""),
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"content": source_content})
        
        result = json.loads(response.content)
        
        return PlatformContent(
            title=result.get("title"),
            content=result.get("content", ""),
            hashtags=[tag.lstrip("#") for tag in result.get("hashtags", [])],
        )
    
    def transform_sync(self, source_content: str, **kwargs) -> PlatformContent:
        """同步转换为知乎格式."""
        import json
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """请将以下内容转换为知乎风格的深度文章：

内容：{content}

请生成：
1. 一个有信息量的标题（50字以内）
2. 深度正文内容（使用结构化表达，分点说明）
3. 2-4个相关话题标签

请以JSON格式输出：
{{"title": "标题", "content": "正文", "hashtags": ["#话题1", "#话题2"]}}
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
=== 知乎平台规则 ===
- 标题：50字以内，可以是问句或陈述句
- 正文：100-5000字，深度、专业、有见地
- 结构：善用列表、分点等结构化表达
- 标签：使用#号，2-4个相关话题
- 图片：支持插入图片增强说服力
"""
