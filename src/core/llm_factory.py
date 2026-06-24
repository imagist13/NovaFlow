"""LLM 工厂 - 创建和管理 LLM 实例."""

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel

from .config import config


class LLMFactory:
    """LLM 工厂类."""
    
    _instances: dict[str, BaseChatModel] = {}
    
    @classmethod
    def get_llm(
        cls,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> BaseChatModel:
        """获取 LLM 实例."""
        provider = provider or config.llm.provider
        model = model or config.llm.model
        temperature = temperature if temperature is not None else config.llm.temperature
        
        cache_key = f"{provider}:{model}:{temperature}"
        if cache_key in cls._instances:
            return cls._instances[cache_key]
        
        llm = cls._create_llm(provider, model, temperature, **kwargs)
        cls._instances[cache_key] = llm
        return llm
    
    @classmethod
    def _create_llm(
        cls,
        provider: str,
        model: str,
        temperature: float,
        **kwargs
    ) -> BaseChatModel:
        """创建 LLM 实例."""
        if provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=config.llm.api_key or kwargs.get("api_key"),
                base_url=config.llm.base_url or kwargs.get("base_url"),
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model,
                temperature=temperature,
                anthropic_api_key=config.llm.api_key or kwargs.get("api_key"),
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    @classmethod
    def clear_cache(cls):
        """清空 LLM 实例缓存."""
        cls._instances.clear()
