# Game Platform Website

一个基于 Python FastAPI 和 Vue.js 的在线小游戏平台网站，提供多种简单有趣的小游戏。

## 项目概述

这是一个使用 FastAPI + Vue.js 开发的在线游戏平台，用户可以在这里玩各种简单的网页小游戏。项目的主要目标是创建一个轻量级、易于扩展的游戏平台，支持多人在线对战和游戏记录保存等功能。

## 技术栈

### 后端技术
- 框架：FastAPI
- 数据库：PostgreSQL
- ORM：SQLAlchemy
- 文档：Swagger UI/ReDoc (自动生成)
- WebSocket：用于实时游戏通信
- 认证：JWT (JSON Web Tokens)
- 容器化：Docker

### 前端技术
- 框架：Vue.js 3
- 构建工具：Vite
- UI框架：Element Plus
- 状态管理：Pinia
- HTTP客户端：Axios
- WebSocket客户端：原生 WebSocket API
- 容器化：Docker

## 主要功能

1. 用户系统
   - 用户注册/登录
   - 个人信息管理
   - 游戏记录统计

2. 游戏功能
   - 五子棋对战
   - 游戏大厅
   - 实时对战系统
   - 排行榜系统

3. 社交功能
   - 好友系统
   - 实时聊天
   - 对战邀请

## 项目结构

```
gobang2/
├── backend/
│   ├── app/
│   │   ├── models/          # 数据模型
│   │   ├── routes/          # API路由
│   │   ├── services/        # 业务逻辑
│   │   └── websockets/      # WebSocket处理
│   ├── config.py            # 配置文件
│   ├── Dockerfile          # 后端 Docker 配置
│   └── requirements.txt     # Python依赖
├── frontend/
│   ├── static/
│   │   ├── css/            # 样式文件
│   │   ├── js/             # JavaScript文件
│   │   └── images/         # 图片资源
│   ├── templates/          # HTML模板
│   └── Dockerfile          # 前端 Docker 配置
├── docker-compose.yml  # Docker Compose 配置
├── tests/                  # 测试文件
└── README.md              # 项目文档
```

## 开发环境要求

- Docker
- Docker Compose

## 快速开始

1. 克隆项目
```bash
git clone https://github.com/yourusername/gobang2.git
cd gobang2
```

2. 使用 Docker Compose 启动服务
```bash
# 构建并启动所有服务
docker-compose up --build

# 后台运行
docker-compose up -d
```

3. 访问服务
- 后端 API 文档：http://localhost:8000/docs
- 前端页面：http://localhost:5173

## 开发指南

### 目录结构
```
gobang2/
├── backend/             # 后端代码
│   ├── app/
│   ├── Dockerfile      # 后端 Docker 配置
│   └── requirements.txt
├── frontend/           # 前端代码
│   ├── src/
│   └── Dockerfile      # 前端 Docker 配置
├── docker-compose.yml  # Docker Compose 配置
└── README.md
```

### 常用 Docker 命令

1. 构建服务
```bash
docker-compose build
```

2. 启动服务
```bash
docker-compose up
```

3. 停止服务
```bash
docker-compose down
```

4. 查看日志
```bash
docker-compose logs -f
```

5. 进入容器
```bash
# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh
```

6. 重新构建并启动特定服务
```bash
docker-compose up --build backend  # 仅重建后端
docker-compose up --build frontend # 仅重建前端
```

### 数据持久化
- PostgreSQL 数据保存在 Docker volume 中
- 代码通过 volume 映射到容器中，支持热重载

## 开发计划

### 第一阶段：基础架构
- [x] 项目初始化
- [ ] 基础框架搭建
- [ ] 数据库设计
- [ ] 用户认证系统

### 第二阶段：游戏核心
- [ ] 五子棋游戏逻辑实现
- [ ] WebSocket通信
- [ ] 游戏匹配系统

### 第三阶段：功能完善
- [ ] 排行榜系统
- [ ] 好友系统
- [ ] 实时聊天

### 第四阶段：优化升级
- [ ] 性能优化
- [ ] UI/UX改进
- [ ] 新游戏接入

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 开源协议

MIT License