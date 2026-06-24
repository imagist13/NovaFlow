"""平台注册表 - 管理所有可用平台."""

from typing import Dict, Type, List
from .base_platform import BasePlatform
from .xiaohongshu import XiaoHongShuPlatform
from .douyin import DouYinPlatform
from .zhihu import ZhiHuPlatform
from .taobao import TaoBaoPlatform


class PlatformRegistry:
    """平台注册表."""
    
    _platforms: Dict[str, Type[BasePlatform]] = {
        "xiaohongshu": XiaoHongShuPlatform,
        "douyin": DouYinPlatform,
        "zhihu": ZhiHuPlatform,
        "taobao": TaoBaoPlatform,
    }
    
    @classmethod
    def register(cls, name: str, platform_class: Type[BasePlatform]):
        """注册新平台."""
        cls._platforms[name] = platform_class
    
    @classmethod
    def get(cls, name: str) -> BasePlatform:
        """获取平台实例."""
        if name not in cls._platforms:
            raise ValueError(f"Unknown platform: {name}")
        return cls._platforms[name]()
    
    @classmethod
    def list_platforms(cls) -> List[str]:
        """列出所有可用平台."""
        return list(cls._platforms.keys())
    
    @classmethod
    def get_all_configs(cls) -> Dict[str, dict]:
        """获取所有平台配置."""
        configs = {}
        for name in cls._platforms:
            platform = cls.get(name)
            configs[name] = platform.config.model_dump()
        return configs
