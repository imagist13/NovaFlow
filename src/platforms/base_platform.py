"""Base Platform - 平台适配器基类."""

from abc import ABC, abstractmethod
from typing import Any, Optional, List
from pydantic import BaseModel, Field


class PlatformConfig(BaseModel):
    """平台配置."""
    name: str
    display_name: str
    max_title_length: int = 100
    max_content_length: int = 2000
    min_content_length: int = 10
    allow_images: bool = True
    allow_hashtags: bool = True
    allow_mentions: bool = True
    require_title: bool = True


class PlatformContent(BaseModel):
    """平台内容."""
    title: Optional[str] = None
    content: str
    images: List[str] = Field(default_factory=list)
    hashtags: List[str] = Field(default_factory=list)
    mentions: List[str] = Field(default_factory=list)


class BasePlatform(ABC):
    """平台适配器基类."""
    
    config: PlatformConfig
    
    @abstractmethod
    def transform(self, source_content: str, **kwargs) -> PlatformContent:
        """将源内容转换为平台适配格式."""
        pass
    
    @abstractmethod
    def validate(self, content: PlatformContent) -> bool:
        """验证内容是否符合平台规范."""
        pass
    
    @abstractmethod
    def get_platform_rules(self) -> str:
        """获取平台规则说明."""
        pass
    
    def format_output(self, content: PlatformContent) -> str:
        """格式化输出."""
        output_parts = []
        
        if content.title:
            output_parts.append(f"标题: {content.title}")
        
        output_parts.append(f"\n内容:\n{content.content}")
        
        if content.hashtags:
            output_parts.append(f"\n标签: {' '.join(['#' + tag for tag in content.hashtags])}")
        
        if content.mentions:
            output_parts.append(f"\n提及: {' '.join(['@' + mention for mention in content.mentions])}")
        
        return "\n".join(output_parts)
