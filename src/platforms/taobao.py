"""淘宝平台适配器."""

from typing import List
from pydantic import Field

from .base_platform import BasePlatform, PlatformConfig, PlatformContent
from ..core.llm_factory import LLMFactory


class TaoBaoPlatform(BasePlatform):
    """淘宝平台适配器."""
    
    config = PlatformConfig(
        name="taobao",
        display_name="淘宝",
        max_title_length=30,
        max_content_length=2000,
        min_content_length=50,
        allow_images=True,
        allow_hashtags=False,
        allow_mentions=False,
        require_title=True,
    )
    
    SYSTEM_PROMPT = """你是一个专业的淘宝内容创作者，擅长创作吸引买家的商品文案。
    
    淘宝特点：
    - 标题突出卖点、关键词
    - 内容强调产品特点和优势
    - 善用促销信息和信任背书
    - 避免过多标签，注重实用性
    - 语气亲切但专业
    
    请根据原始内容创作适合淘宝风格的商品文案。"""
    
    def __init__(self):
        self.llm = LLMFactory.get_llm()
    
    async def transform(self, source_content: str, **kwargs) -> PlatformContent:
        """转换为淘宝格式."""
        from langchain_core.prompts import ChatPromptTemplate
        import json
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """请将以下内容转换为淘宝风格的商品文案：

内容：{content}

请生成：
1. 一个突出卖点的标题（30字以内，含关键词）
2. 商品详情文案（强调特点和优势）
3. 促销信息或信任背书（可选）

请以JSON格式输出：
{{"title": "标题", "content": "详情文案"}}
"""),
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"content": source_content})
        
        result = json.loads(response.content)
        
        return PlatformContent(
            title=result.get("title"),
            content=result.get("content", ""),
        )
    
    def transform_sync(self, source_content: str, **kwargs) -> PlatformContent:
        """同步转换为淘宝格式."""
        import json
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """请将以下内容转换为淘宝风格的商品文案：

内容：{content}

请生成：
1. 一个突出卖点的标题（30字以内，含关键词）
2. 商品详情文案（强调特点和优势）
3. 促销信息或信任背书（可选）

请以JSON格式输出：
{{"title": "标题", "content": "详情文案"}}
"""),
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"content": source_content})
        
        result = json.loads(response.content)
        
        return PlatformContent(
            title=result.get("title"),
            content=result.get("content", ""),
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
=== 淘宝平台规则 ===
- 标题：30字以内，突出卖点和关键词
- 详情：50-2000字，强调产品特点和优势
- 图片：支持多图，建议白底主图+详情图
- 标签：无需标签，注重实用性
- 信任背书：可添加售后保障、销量等信息
"""
