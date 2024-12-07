#!/bin/sh

# 启动 FastAPI 服务器在后台
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

# 将控制权交给 CMD
exec "$@"
