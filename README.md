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

## API 设计

### 认证相关 (/api/auth)
```
POST /api/auth/register         # 用户注册
POST /api/auth/login           # 用户登录
POST /api/auth/logout          # 用户登出
GET  /api/auth/me              # 获取当前用户信息
PUT  /api/auth/me              # 更新当前用户信息
```

### 游戏相关 (/api/game)
```
GET    /api/game/rooms                # 获取游戏房间列表
POST   /api/game/rooms                # 创建游戏房间
GET    /api/game/rooms/{room_id}      # 获取特定房间信息
DELETE /api/game/rooms/{room_id}      # 删除游戏房间
POST   /api/game/rooms/{room_id}/join # 加入游戏房间
POST   /api/game/rooms/{room_id}/move # 下棋
```

### 匹配系统 (/api/matchmaking)
```
POST   /api/matchmaking/queue         # 加入匹配队列
DELETE /api/matchmaking/queue         # 退出匹配队列
GET    /api/matchmaking/status        # 获取匹配状态
```

### WebSocket 端点
```
WS  /ws/game/{room_id}               # 游戏房间的 WebSocket 连接
WS  /ws/matchmaking                  # 匹配系统的 WebSocket 连接
```

### 排行榜 (/api/leaderboard)
```
GET  /api/leaderboard/global         # 获取全球排行榜
GET  /api/leaderboard/friends        # 获取好友排行榜
```

### 用户资料 (/api/users)
```
GET    /api/users/{user_id}          # 获取用户信息
PUT    /api/users/{user_id}          # 更新用户信息
GET    /api/users/{user_id}/stats    # 获取用户战绩
```

### 好友系统 (/api/friends)
```
GET    /api/friends                  # 获取好友列表
POST   /api/friends/requests         # 发送好友请求
GET    /api/friends/requests         # 获取好友请求列表
PUT    /api/friends/requests/{id}    # 处理好友请求
DELETE /api/friends/{friend_id}      # 删除好友
```

### WebSocket 事件
```javascript
// 游戏事件
{
    "type": "game_start",
    "data": { ... }
}
{
    "type": "game_move",
    "data": {
        "position": [x, y],
        "player": "player_id"
    }
}
{
    "type": "game_end",
    "data": {
        "winner": "player_id",
        "reason": "win/surrender/timeout"
    }
}

// 匹配事件
{
    "type": "match_found",
    "data": {
        "room_id": "room_id",
        "opponent": {
            "id": "player_id",
            "username": "username"
        }
    }
}

// 系统事件
{
    "type": "error",
    "data": {
        "code": "error_code",
        "message": "error_message"
    }
}
```

### 数据模型

#### User
```python
class User(Base):
    id: UUID
    username: str
    email: str
    password_hash: str
    rating: int
    games_played: int
    games_won: int
    created_at: datetime
    updated_at: datetime
```

#### GameRoom
```python
class GameRoom(Base):
    id: UUID
    player1_id: UUID
    player2_id: UUID
    current_turn: UUID
    status: str  # waiting/playing/finished
    winner_id: UUID
    board: List[List[int]]
    created_at: datetime
    updated_at: datetime
```

#### GameMove
```python
class GameMove(Base):
    id: UUID
    game_id: UUID
    player_id: UUID
    position_x: int
    position_y: int
    created_at: datetime
```

#### FriendRequest
```python
class FriendRequest(Base):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    status: str  # pending/accepted/rejected
    created_at: datetime
    updated_at: datetime
```

### 开发优先级

1. 第一阶段：基础功能
   - 用户认证 (register, login, me)
   - 基本的游戏房间管理
   - WebSocket 连接

2. 第二阶段：游戏核心
   - 游戏逻辑实现
   - 房间管理完善
   - 对局记录

3. 第三阶段：匹配系统
   - 玩家匹配
   - 排行榜

4. 第四阶段：社交功能
   - 好友系统
   - 观战功能

## 当前进度
- [x] 项目基础架构搭建
- [x] Docker 环境配置
- [x] 前后端服务基本框架

## 下一步计划
1. 开始用户系统开发
   - 设计用户模型
   - 实现注册接口
   - 实现登录接口
   - 添加 JWT 认证

2. 准备开发任务
   - 创建数据库迁移
   - 设置 API 路由
   - 创建前端页面组件
   - 实现前后端通信

## 开发规范
1. Git 提交规范
   - feat: 新功能
   - fix: 修复
   - docs: 文档
   - style: 格式
   - refactor: 重构
   - test: 测试
   - chore: 构建

2. 代码规范
   - Python: PEP 8
   - Vue: Vue Style Guide
   - 使用 TypeScript
   - 编写单元测试

3. API 规范
   - RESTful 设计
   - 版本控制
   - 错误处理
   - 文档完备

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 开源协议

MIT License