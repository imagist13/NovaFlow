# NovaFlow Web 前端

NovaFlow 的 Next.js Web 界面，提供简洁美观的用户体验。

## 功能特性

- 🎨 **简约设计** - 现代化 UI，美观大方
- 📱 **响应式布局** - 适配各种设备
- ⚡ **实时预览** - 即时生成内容预览
- 🔄 **一键复制** - 方便快捷的内容复制
- 🎯 **多平台支持** - 同时适配多个平台

## 快速开始

### 安装依赖

```bash
cd web
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 [http://localhost:3000](http://localhost:3000)

### 构建生产版本

```bash
npm run build
npm start
```

## 项目结构

```
web/
├── app/
│   ├── api/
│   │   └── adapt/
│   │       └── route.ts    # 适配 API
│   ├── globals.css         # 全局样式
│   ├── layout.tsx          # 布局
│   └── page.tsx            # 主页面
├── components/
│   ├── ContentInput.tsx    # 内容输入组件
│   ├── PlatformSelector.tsx # 平台选择组件
│   └── ContentDisplay.tsx  # 结果展示组件
├── public/                 # 静态资源
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## 技术栈

- **Next.js 14** - React 框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式设计
- **API Routes** - 后端接口

## 使用说明

1. 在左侧输入原始内容
2. 选择目标平台（可多选）
3. 点击"开始适配"按钮
4. 在右侧查看生成的适配内容
5. 点击复制按钮获取内容

## 注意事项

- 确保后端服务已启动（端口 8000）
- API 路由目前返回模拟数据，需对接真实后端
- 建议使用现代浏览器以获得最佳体验

## 许可证

MIT License
