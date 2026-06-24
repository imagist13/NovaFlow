"""抖音平台适配器."""

from typing import List
from pydantic import Field

from .base_platform import BasePlatform, PlatformConfig, PlatformContent
from ..core.llm_factory import LLMFactory


class DouYinPlatform(BasePlatform):
    """抖音平台适配器."""
    
    config = PlatformConfig(
        name="douyin",
        display_name="抖音",
        max_title_length=30,
        max_content_length=500,
        min_content_length=20,
        allow_images=False,
        allow_hashtags=True,
        allow_mentions=True,
        require_title=True,
    )
    
    SYSTEM_PROMPT = """你是一个专业的抖音内容创作者，擅长创作吸引人的短视频脚本和文案。
    
    抖音特点：
    - 标题简短有力，抓住眼球
    - 内容简洁、直击要点
    - 善用悬念和反转
    - 标签使用#号，热门标签效果好
    - 语气有感染力，适合短视频节奏
    
    请根据原始内容创作适合抖音风格的文案。"""
    
    def __init__(self):
        self.llm = LLMFactory.get_llm()
    
    async def transform(self, source_content: str, **kwargs) -> PlatformContent:
        """转换为抖音格式."""
        from langchain_core.prompts import ChatPromptTemplate
        import json
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """请将以下内容转换为抖音风格的短视频文案：

内容：{content}

请生成：
1. 一个吸引人的标题（30字以内，制造悬念）
2. 短视频口播文案（简洁有力，适合15-60秒视频）
3. 3-5个热门标签

请以JSON格式输出：
{{"title": "标题", "content": "口播文案", "hashtags": ["#标签1", "#标签2"]}}
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
        """同步转换为抖音格式."""
        import json
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """请将以下内容转换为抖音风格的短视频文案：

内容：{content}

请生成：
1. 一个吸引人的标题（30字以内，制造悬念）
2. 短视频口播文案（简洁有力，适合15-60秒视频）
3. 3-5个热门标签

请以JSON格式输出：
{{"title": "标题", "content": "口播文案", "hashtags": ["#标签1", "#标签2"]}}
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
=== 抖音平台规则 ===
- 标题：30字以内，制造悬念和好奇心
- 口播文案：20-500字，简洁有力
- 标签：使用#号，3-5个热门标签
- 内容：适合短视频节奏，直击要点
- 互动：结尾引导评论和分享
"""
