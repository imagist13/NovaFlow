"""Base Agent - 所有 Agent 的基类."""

from abc import ABC, abstractmethod
from typing import Any, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

from ..core.llm_factory import LLMFactory


class BaseAgent(ABC):
    """Agent 基类."""
    
    def __init__(
        self,
        name: str,
        description: str,
        system_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature
        self.llm = LLMFactory.get_llm(model=model, temperature=temperature)
        self._setup_prompt()
    
    def _setup_prompt(self):
        """设置提示模板."""
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}"),
        ])
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """处理输入数据."""
        pass
    
    async def invoke(self, input_text: str, **kwargs) -> str:
        """同步调用 Agent."""
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"input": input_text, **kwargs})
        return response.content
    
    def sync_invoke(self, input_text: str, **kwargs) -> str:
        """同步调用 Agent."""
        chain = self.prompt | self.llm
        response = chain.invoke({"input": input_text, **kwargs})
        return response.content
