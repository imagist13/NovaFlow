# NovaFlow

<div align="center">

![NovaFlow Logo](https://img.shields.io/badge/NovaFlow-AI%20Content%20Adapter-0EA5E9?style=for-the-badge&logo=rocket)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-FF6B6B?style=for-the-badge)

*基于多 Agent 架构的智能多平台内容适配工具*

[功能特性](#功能特性) • [快速开始](#快速开始) • [项目结构](#项目结构) • [使用指南](#使用指南) • [开发文档](#开发文档)

</div>

---

## ✨ 功能特性

<div align="center">

| 特性 | 说明 |
|:---|:---|
| 🎯 **多平台支持** | 支持小红书、抖音、知乎、淘宝等主流平台 |
| 🤖 **AI 智能适配** | 自动识别内容特点，转换为各平台最佳格式 |
| 🧩 **模块化设计** | 平台规则可扩展，方便添加新平台 |
| 💻 **CLI + Web** | 命令行工具开箱即用，也可扩展 Web 界面 |
| 🔗 **LangChain** | 基于 LangChain 实现，灵活可扩展 |

</div>

---

## 🚀 快速开始

### 📦 安装

```bash
# 克隆项目
git clone <repository-url>
cd novaflow

# 安装 Python 依赖
pip install -r requirements.txt
```

### ⚙️ 配置

```bash
# 复制环境变量配置
cp .env.example .env
```

编辑 `.env` 文件：

```env
# OpenAI API 配置
OPENAI_API_KEY=your_api_key_here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
```

### 🎮 使用

#### 命令行模式

```bash
# 列出所有可用平台
python novaflow.py list-platforms

# 查看平台规则
python novaflow.py platform-info xiaohongshu

# 适配内容到多个平台
python novaflow.py adapt --content "你的内容" --platforms "xiaohongshu,douyin"

# 交互式模式
python novaflow.py interactive
```

#### Web 界面

```bash
cd web
npm install
npm run dev
```

访问 `http://localhost:3000`

---

## 📁 项目结构

```
novaflow/
│
├── 🐍 Python 后端
│   └── src/
│       ├── agents/              # Agent 模块
│       │   └── base_agent.py   # Agent 基类
│       │
│       ├── platforms/           # 平台适配器
│       │   ├── base_platform.py    # 平台基类
│       │   ├── xiaohongshu.py   # 小红书适配器
│       │   ├── douyin.py        # 抖音适配器
│       │   ├── zhihu.py         # 知乎适配器
│       │   ├── taobao.py        # 淘宝适配器
│       │   └── registry.py      # 平台注册表
│       │
│       ├── core/                # 核心功能
│       │   ├── config.py        # 配置管理
│       │   └── llm_factory.py   # LLM 工厂
│       │
│       ├── utils/               # 工具模块
│       ├── cli.py              # CLI 入口
│       └── main.py             # 主入口
│
├── 🌐 Web 前端
│   └── web/
│       ├── app/                # Next.js App
│       ├── components/         # React 组件
│       └── package.json
│
├── 📋 配置文件
│   ├── pyproject.toml          # Python 项目配置
│   ├── requirements.txt        # Python 依赖
│   ├── .env.example           # 环境变量示例
│   └── .gitignore
│
└── 📚 文档
    ├── README.md
    └── tests/                  # 测试文件
```

---

## 📋 支持的平台

<div align="center">

| 平台 | 标识 | 最大标题 | 最大内容 | 特点 |
|:---:|:---:|:---:|:---:|:---|
| 📕 小红书 | `xiaohongshu` | 20字 | 1000字 | 种草分享、图文笔记 |
| 🎵 抖音 | `douyin` | 30字 | 500字 | 短视频口播、悬念文案 |
| 💬 知乎 | `zhihu` | 50字 | 5000字 | 深度内容、专业问答 |
| 🛒 淘宝 | `taobao` | 30字 | 2000字 | 商品详情、营销文案 |

</div>

---

## 📖 使用指南

### 1️⃣ 基本用法

```python
from src.platforms.registry import PlatformRegistry

# 获取平台
platform = PlatformRegistry.get("xiaohongshu")

# 转换内容
result = platform.transform_sync("你的原始内容")

# 格式化输出
print(platform.format_output(result))
```

### 2️⃣ 添加新平台

```python
# 1. 创建平台文件 src/platforms/myplatform.py
from .base_platform import BasePlatform, PlatformConfig, PlatformContent

class MyPlatform(BasePlatform):
    config = PlatformConfig(
        name="myplatform",
        display_name="我的平台",
        max_title_length=50,
        max_content_length=1000,
    )
    
    def transform(self, source_content: str, **kwargs) -> PlatformContent:
        # 实现转换逻辑
        pass
    
    def validate(self, content: PlatformContent) -> bool:
        # 实现验证逻辑
        pass

# 2. 在 registry.py 中注册
from .myplatform import MyPlatform
PlatformRegistry.register("myplatform", MyPlatform)
```

---

## 🛠️ 开发文档

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio

# 运行测试
pytest tests/ -v
```

### 代码规范

```bash
# 格式化代码
black src/

# 检查代码
ruff check src/
```

---

## 📝 License

<div align="center">

MIT License - 随时欢迎贡献！

</div>

---

<div align="center">

**Made with ❤️ by NovaFlow Team**

</div>
