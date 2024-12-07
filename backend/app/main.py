from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .api.endpoints import auth, game, ws

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Game Platform API",
    description="Game Platform RESTful API documentation",
    version="1.0.0"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(game.router, prefix="/api/game", tags=["game"])
app.include_router(ws.router, prefix="/ws", tags=["websocket"])

@app.get("/")
async def root():
    return {"message": "Welcome to Game Platform API"}
