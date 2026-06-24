"""NovaFlow 测试."""

import pytest
from src.platforms.registry import PlatformRegistry
from src.platforms.base_platform import PlatformContent


def test_list_platforms():
    """测试平台列表."""
    platforms = PlatformRegistry.list_platforms()
    assert len(platforms) >= 4
    assert "xiaohongshu" in platforms
    assert "douyin" in platforms
    assert "zhihu" in platforms
    assert "taobao" in platforms


def test_get_platform():
    """测试获取平台."""
    platform = PlatformRegistry.get("xiaohongshu")
    assert platform is not None
    assert platform.config.name == "xiaohongshu"


def test_invalid_platform():
    """测试无效平台."""
    with pytest.raises(ValueError):
        PlatformRegistry.get("invalid_platform")


def test_platform_validation():
    """测试平台验证."""
    platform = PlatformRegistry.get("xiaohongshu")
    
    valid_content = PlatformContent(
        title="测试标题",
        content="这是一段测试内容，长度足够通过验证",
        hashtags=["测试", "内容"],
    )
    assert platform.validate(valid_content) is True
    
    invalid_content = PlatformContent(
        title="测试",
        content="太短",
    )
    assert platform.validate(invalid_content) is False


def test_format_output():
    """测试输出格式化."""
    platform = PlatformRegistry.get("xiaohongshu")
    content = PlatformContent(
        title="测试标题",
        content="测试内容",
        hashtags=["tag1", "tag2"],
    )
    
    output = platform.format_output(content)
    assert "标题: 测试标题" in output
    assert "测试内容" in output
    assert "#tag1" in output
    assert "#tag2" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
