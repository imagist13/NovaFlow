"""NovaFlow 配置管理."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class LLMConfig(BaseModel):
    """LLM 配置."""
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    api_key: Optional[str] = None
    base_url: Optional[str] = None


class NovaFlowConfig(BaseModel):
    """NovaFlow 全局配置."""
    llm: LLMConfig = LLMConfig()
    max_retries: int = 3
    timeout: int = 60
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "NovaFlowConfig":
        """从环境变量加载配置."""
        return cls(
            llm=LLMConfig(
                provider=os.getenv("LLM_PROVIDER", "openai"),
                model=os.getenv("LLM_MODEL", "gpt-4"),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL"),
            ),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            timeout=int(os.getenv("TIMEOUT", "60")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


config = NovaFlowConfig.from_env()
